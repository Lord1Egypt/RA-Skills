"""Application entry point for the ACP-to-OpenAI Bridge.

Creates the FastAPI application, manages startup/shutdown lifecycle
(ProcessManager, SessionManager initialization), and runs the uvicorn server.
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from acp_openai_bridge.config import BridgeConfig, detect_platform, find_kiro_cli
from acp_openai_bridge.process_manager import ProcessManager
from acp_openai_bridge.response_translator import ResponseTranslator
from acp_openai_bridge.routes import router
from acp_openai_bridge.session_manager import SessionManager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown lifecycle.

    Startup:
        1. Load BridgeConfig from app.state (set by create_app).
        2. Detect platform and log the result.
        3. Resolve kiro_cli_path: use config value or find_kiro_cli().
        4. Resolve cwd: use config value or os.getcwd().
        5. Create ProcessManager and start the ACP subprocess.
        6. Create SessionManager and initialize a session.
        7. Store ProcessManager, SessionManager, and config in app.state.
        8. Print startup message with host:port.

    Shutdown:
        1. Call ProcessManager.shutdown() to gracefully stop the subprocess.
    """
    config: BridgeConfig = app.state.config

    # 1. Detect platform and log
    platform_info = detect_platform()
    logger.info(
        "Platform detected: system=%s, is_wsl=%s, machine=%s",
        platform_info["system"],
        platform_info["is_wsl"],
        platform_info["machine"],
    )

    # 2. Resolve kiro-cli path
    kiro_cli_path = config.kiro_cli_path or find_kiro_cli()
    logger.info("Using kiro-cli at: %s", kiro_cli_path)

    # 3. Resolve working directory
    cwd = config.cwd or os.getcwd()
    logger.info("Working directory: %s", cwd)

    # 4. Create ProcessManager and start subprocess
    process_manager = ProcessManager(kiro_cli_path, cwd, model=config.model)
    await process_manager.start()

    # 5. Create SessionManager and initialize session
    session_manager = SessionManager(process_manager.writer, process_manager.reader)
    await session_manager.create_session(cwd)

    # 6. Store instances in app.state for route access
    app.state.process_manager = process_manager
    app.state.session_manager = session_manager

    # 7. Print startup message
    print(f"ACP-to-OpenAI Bridge running at http://{config.host}:{config.port}")

    yield

    # Shutdown: gracefully stop the ACP subprocess
    logger.info("Shutting down ACP subprocess...")
    await process_manager.shutdown()
    logger.info("ACP subprocess shut down successfully")


def create_app(config: BridgeConfig) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        config: The bridge configuration to use.

    Returns:
        A configured FastAPI application instance.
    """
    app = FastAPI(
        title="ACP-to-OpenAI Bridge",
        description="Local proxy translating OpenAI requests to ACP JSON-RPC",
        lifespan=lifespan,
    )

    # Store config in app.state before lifespan runs
    app.state.config = config

    # Global exception handler for unhandled exceptions
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Catch any unhandled exceptions and return OpenAI error format."""
        logger.exception("Unhandled exception: %s", exc)
        error = ResponseTranslator.to_error_response(
            message="Internal server error",
            error_type="server_error",
            code="internal_error",
        )
        return JSONResponse(content=error, status_code=500)

    # Include API routes
    app.include_router(router)

    return app


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    # Quiet down noisy libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    # Parse config before creating the app to avoid argparse/uvicorn conflicts
    config = BridgeConfig.from_args_and_env()
    app = create_app(config)

    uvicorn.run(app, host=config.host, port=config.port)
