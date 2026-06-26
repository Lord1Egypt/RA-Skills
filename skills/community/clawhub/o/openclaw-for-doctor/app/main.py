from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, status

from app.channels.dispatcher import ChannelDispatcher
from app.config import Settings, get_settings
from app.core.engine import DoctorAssistantEngine
from app.core.models import HealthStatus, StoredTask, TaskRequest, TaskResult, TaskStatus
from app.services.async_executor import AsyncTaskExecutor
from app.services.base import TaskManager
from app.services.task_store_factory import create_task_manager

settings: Settings = get_settings()
engine = DoctorAssistantEngine()
task_manager: TaskManager = create_task_manager(settings)
dispatcher = ChannelDispatcher()
executor = AsyncTaskExecutor(task_manager=task_manager, engine=engine, dispatcher=dispatcher, settings=settings)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    executor.start()
    try:
        yield
    finally:
        executor.stop()


app = FastAPI(title="openclaw-for-doctor", version="0.1.0", lifespan=lifespan)


@app.get("/api/health", response_model=HealthStatus)
def health() -> HealthStatus:
    return HealthStatus(env=settings.env, task_store=settings.task_store)


def require_auth(x_doctor_token: Optional[str] = Header(default=None)) -> None:
    if not settings.api_token:
        return
    if x_doctor_token != settings.api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing X-Doctor-Token",
        )


@app.post("/api/tasks/execute", response_model=TaskResult)
def execute_task(request: TaskRequest, _auth: None = Depends(require_auth)) -> TaskResult:
    result = engine.execute(request)
    result.delivery = dispatcher.dispatch(request.channel, result)
    return result


@app.post("/api/tasks/submit", response_model=StoredTask)
def submit_task(request: TaskRequest, _auth: None = Depends(require_auth)) -> StoredTask:
    task = task_manager.create(request)
    profile = engine.build_profile(request)
    task_manager.set_profile(task.task_id, profile)
    task_manager.mark_running(task.task_id)

    try:
        result = engine.execute(request, task_id=task.task_id)
        result.delivery = dispatcher.dispatch(request.channel, result)
        task_manager.mark_completed(task.task_id, result)
    except Exception as exc:
        task_manager.mark_failed(task.task_id, str(exc))

    return task_manager.get(task.task_id)


@app.post("/api/tasks/submit-async", response_model=StoredTask)
def submit_task_async(request: TaskRequest, _auth: None = Depends(require_auth)) -> StoredTask:
    task = task_manager.create(request)
    profile = engine.build_profile(request)
    task_manager.set_profile(task.task_id, profile)
    executor.start()
    executor.enqueue(task.task_id)
    return task_manager.get(task.task_id)


@app.post("/api/tasks/{task_id}/cancel", response_model=StoredTask)
def cancel_task(task_id: str, _auth: None = Depends(require_auth)) -> StoredTask:
    try:
        task = task_manager.get(task_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"task {task_id} not found") from exc

    if task.status == TaskStatus.running:
        raise HTTPException(status_code=409, detail="running task cannot be cancelled")
    if task.status == TaskStatus.completed:
        raise HTTPException(status_code=409, detail="completed task cannot be cancelled")
    if task.status == TaskStatus.cancelled:
        return task

    task_manager.mark_cancelled(task_id, "Cancelled by user request.")
    return task_manager.get(task_id)


@app.post("/api/tasks/{task_id}/retry", response_model=StoredTask)
def retry_task(task_id: str, _auth: None = Depends(require_auth)) -> StoredTask:
    try:
        task = task_manager.get(task_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"task {task_id} not found") from exc

    if task.status not in {TaskStatus.failed, TaskStatus.cancelled}:
        raise HTTPException(status_code=409, detail="only failed/cancelled tasks can be retried")

    task_manager.requeue(task_id)
    executor.start()
    executor.enqueue(task_id)
    return task_manager.get(task_id)


@app.get("/api/tasks/{task_id}", response_model=StoredTask)
def get_task(task_id: str, _auth: None = Depends(require_auth)) -> StoredTask:
    try:
        return task_manager.get(task_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"task {task_id} not found") from exc


@app.get("/api/tasks", response_model=list[StoredTask])
def list_tasks(_auth: None = Depends(require_auth)) -> list[StoredTask]:
    return task_manager.list()
