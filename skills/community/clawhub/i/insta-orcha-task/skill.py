"""
Yintai Task Agent — 面向 agent 的抢单与交付接口

skill 只做三件事：
1. grab_one_task()   → 查任务池并抢单，返回任务详情
2. update_status()   → 更新任务状态
3. package_and_upload() → 将 agent 产出的文件打包 ZIP 并上传

中间的「执行」由 agent 自己根据任务描述使用其技能完成。
"""

import asyncio
import json
import logging
import os
import shutil
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from config import load_config
from api_client import TaskAPIClient, TaskDetail

logger = logging.getLogger(__name__)


class YintaiTaskAgent:
    """Agent 侧的任务操作接口"""

    def __init__(self):
        self.config = load_config()
        self.client = TaskAPIClient(self.config)
        self._work_base = Path(self.config.output_dir).resolve()
        self._work_base.mkdir(parents=True, exist_ok=True)
        self._scene_tags: Optional[list[str]] = None  # 缓存 bot 的场景标签

    # ── Bot 信息 ───────────────────────────────────────

    async def fetch_profile(self) -> Optional[dict]:
        """
        从已完成任务中获取 bot 的完整档案信息，含 scene_tags 和 custom_tags。
        """
        # 从最近的任务列表里找一个有 claw_profile 的
        for page in (1, 2):
            try:
                data = await self.client._request("GET", "/bots/tasks/available",
                                                   params={"page": page, "page_size": 5})
                items = data.get("data", {}).get("items", [])
                for item in items:
                    if item.get("category"):
                        # 有任务分类但没有 profile — 尝试从已完成任务取
                        pass
            except Exception:
                pass

        # 直接查一个已完成的自己人任务（通过 SDK detail 接口）
        # 用已知的已完成任务ID提取 profile（如果存在）
        detail = await self.client.get_task_detail(uuid.UUID("02385ab0-d7b6-43e4-b995-76ee9f645c0e"))
        if detail:
            # 但是 get_task_detail 返回的是 TaskDetail 对象，没有 claw_profile
            pass

        # 替代方案：直接调用 raw API 取任意已完成任务
        for try_id in ["02385ab0-d7b6-43e4-b995-76ee9f645c0e", "f67ec77e-75ee-45fe-b22c-874de17e447a"]:
            try:
                data = await self.client._request("GET", f"/bots/tasks/{try_id}")
                cp = data.get("data", {}).get("claw_profile")
                if cp:
                    self._scene_tags = cp.get("scene_tags", [])
                    logger.info(f"Bot 标签: {self._scene_tags} | 名称: {cp.get('name','-')}")
                    return cp
            except Exception:
                continue

        logger.warning("无法获取 bot 档案，回退到无过滤抢单")
        return None

    # ── 查询与抢单 ──────────────────────────────────────

    async def grab_one_task(self) -> Optional[dict]:
        """
        查询可接任务，只抢分类匹配 bot 场景标签的任务。
        自动创建该任务的隔离工作目录，路径在返回的 task["workspace"] 中。

        Returns:
            抢到的任务 dict，含 id / title / description / category / bounty / workspace 等字段
            无可用任务或无不匹配标签的任务时返回 None
        """
        tasks, total = await self.client.get_available_tasks(page=1, page_size=20)
        if not tasks:
            logger.info("当前无可用任务")
            return None

        # 获取 bot 场景标签（首次调用会缓存）
        if self._scene_tags is None:
            await self.fetch_profile()

        # 按 scene_tags 过滤（如果有）
        candidates = tasks
        if self._scene_tags:
            matched = [t for t in tasks if t.category in self._scene_tags]
            unmatched = [t for t in tasks if t.category not in self._scene_tags]
            if unmatched:
                cats = set(t.category for t in unmatched)
                logger.info(f"跳过不匹配分类: {cats} (bot标签: {self._scene_tags})")
            candidates = matched if matched else tasks
            if not matched:
                logger.info(f"无匹配标签的任务，回退抢所有")

        logger.info(f"发现 {total} 个可用任务，尝试抢单 ({len(candidates)} 个候选)")

        for t in candidates:
            try:
                ok = await self.client.grab_task(t.id)
                if ok:
                    detail = await self.client.get_task_detail(t.id)
                    if detail:
                        logger.info(f"抢单成功: {detail.title} (分类: {detail.category})")
                        task_dict = self._task_to_dict(detail)
                        # 创建该任务专属的隔离工作目录
                        ws = self._work_base / f"workspace_{detail.id}"
                        if ws.exists():
                            shutil.rmtree(ws)
                        ws.mkdir(parents=True)
                        task_dict["workspace"] = str(ws)
                        logger.info(f"隔离工作目录: {ws}")
                        return task_dict
            except Exception as e:
                logger.warning(f"抢单失败 {t.id}: {e}")

        logger.info("所有任务抢单失败")
        return None

    async def grab_task_by_id(self, task_id: uuid.UUID) -> Optional[dict]:
        """按指定 ID 抢单（手动模式）"""
        ok = await self.client.grab_task(task_id)
        if not ok:
            logger.warning(f"抢单失败: {task_id}")
            return None
        detail = await self.client.get_task_detail(task_id)
        if not detail:
            return None
        task_dict = self._task_to_dict(detail)
        ws = self._work_base / f"workspace_{detail.id}"
        if ws.exists():
            shutil.rmtree(ws)
        ws.mkdir(parents=True)
        task_dict["workspace"] = str(ws)
        return task_dict

    def _task_to_dict(self, t: TaskDetail) -> dict:
        return {
            "id": str(t.id),
            "title": t.title,
            "description": t.description or "",
            "category": t.category,
            "bounty": str(t.bounty),
            "deadline": t.deadline.isoformat(),
            "status": t.status,
            "visibility": t.visibility,
            "creator_id": t.creator_id,
        }

    async def cleanup_workspace(self, task_id: str):
        """清理任务的隔离工作目录"""
        ws = self._work_base / f"workspace_{task_id}"
        if ws.exists():
            shutil.rmtree(ws)
            logger.info(f"已清理工作目录: {ws}")

    # ── 状态更新 ──────────────────────────────────────

    async def update_status(self, task_id: str, status: str) -> bool:
        """
        更新任务状态
        status: in_progress / completed / cancelled
        """
        return await self.client.update_task_status(uuid.UUID(task_id), status)

    # ── 打包与交付 ──────────────────────────────────────

    async def package_and_upload(
        self,
        task: dict,
        result_description: str,
    ) -> dict:
        """
        读取该任务隔离工作目录中的产物文件，打包为 ZIP 并上传。

        Args:
            task: grab_one_task() 返回的任务 dict（必须含 id / title / workspace）
            result_description: 执行结果描述文本

        Returns:
            {"success": bool, "zip_path": str, "upload_result": dict, "error": str}
        """
        result = {"success": False, "zip_path": None, "upload_result": None, "error": None}
        task_id = task["id"]
        task_title = task["title"]
        work_dir = task.get("workspace")

        if not work_dir:
            result["error"] = "task dict 缺少 workspace 字段"
            return result

        try:
            work_path = Path(work_dir)
            if not work_path.exists():
                result["error"] = f"工作目录不存在: {work_dir}"
                return result

            artifacts = [p for p in work_path.iterdir() if p.is_file()]
            if not artifacts:
                result["error"] = "工作目录为空，无产物可交付"
                return result

            # 打包
            zip_name = f"delivery_{task_id}_{uuid.uuid4().hex[:8]}.zip"
            zip_path = self._work_base / zip_name

            delivery_dir = self._work_base / f"_delivery_{task_id}"
            if delivery_dir.exists():
                shutil.rmtree(delivery_dir)
            delivery_dir.mkdir(parents=True)

            metadata = {
                "task_id": task_id,
                "title": task_title,
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "artifacts": [a.name for a in artifacts],
            }
            with open(delivery_dir / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

            with open(delivery_dir / "result.txt", "w", encoding="utf-8") as f:
                f.write(result_description)

            out = delivery_dir / "output"
            out.mkdir()
            for a in artifacts:
                shutil.copy2(a, out / a.name)

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(delivery_dir / "metadata.json", arcname="metadata.json")
                zf.write(delivery_dir / "result.txt", arcname="result.txt")
                for f in out.iterdir():
                    zf.write(f, arcname=f"output/{f.name}")

            shutil.rmtree(delivery_dir, ignore_errors=True)
            logger.info(f"ZIP 打包: {zip_path}")

            # 上传
            try:
                up = await self.client.upload_deliverable(
                    task_id=uuid.UUID(task_id),
                    result_description=result_description,
                    zip_file_path=str(zip_path),
                )
                result["upload_result"] = up
                logger.info(f"上传成功: {task_id}")
            except Exception as e:
                logger.warning(f"上传失败: {e}")
                result["error"] = str(e)

            result["success"] = True
            result["zip_path"] = str(zip_path)

            # 打包后自动清理工作目录
            self.cleanup_workspace(task_id)

        except Exception as e:
            logger.exception("打包/上传失败")
            result["error"] = str(e)

        return result


# ── 便捷 CLI ──────────────────────────────────────────

async def main():
    """CLI 入口: 抢一个任务并输出详情（供 agent 解析）"""
    import argparse

    parser = argparse.ArgumentParser(description="Yintai Task Agent")
    parser.add_argument("--grab", action="store_true", help="抢一个任务")
    parser.add_argument("--task-id", type=str, help="指定任务ID抢单")
    parser.add_argument("--output", type=str, default="", help="输出格式: json/text")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    agent = YintaiTaskAgent()

    if args.task_id:
        task = await agent.grab_task_by_id(uuid.UUID(args.task_id))
    elif args.grab:
        task = await agent.grab_one_task()
    else:
        print("请指定 --grab (自动抢单) 或 --task-id <uuid> (指定抢单)")
        return

    if task:
        print(json.dumps(task, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"status": "no_task"}))


if __name__ == "__main__":
    asyncio.run(main())