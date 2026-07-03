"""ACP subprocess lifecycle manager.

Manages the kiro-cli acp child process: startup, initialization handshake,
graceful shutdown, and automatic crash recovery.
"""

from __future__ import annotations

import asyncio
import logging

from acp_openai_bridge.acp_reader import ACPReader
from acp_openai_bridge.jsonrpc_writer import JSONRPCWriter

logger = logging.getLogger(__name__)


class ProcessManager:
    """ACP 子进程生命周期管理器

    Manages the full lifecycle of the ``kiro-cli acp`` subprocess:
    starting, performing the JSON-RPC ``initialize`` handshake,
    graceful shutdown, and automatic crash recovery.

    All start/shutdown operations are protected by an ``asyncio.Lock``
    to prevent concurrent lifecycle transitions.
    """

    def __init__(self, kiro_cli_path: str, cwd: str, model: str | None = None) -> None:
        self._kiro_cli_path = kiro_cli_path
        self._cwd = cwd
        self._model = model
        self._process: asyncio.subprocess.Process | None = None
        self._reader: ACPReader | None = None
        self._writer: JSONRPCWriter | None = None
        self._is_available: bool = False
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        """启动 ACP 子进程并完成初始化握手。

        Steps:
        1. Spawn ``kiro-cli acp`` with stdin=PIPE, stdout=PIPE.
        2. Create :class:`ACPReader` and :class:`JSONRPCWriter` instances.
        3. Start the reader's background read loop.
        4. Send the ``initialize`` JSON-RPC request and wait for the response.
        5. Mark the process as available.

        The entire operation is protected by ``self._lock``.
        """
        async with self._lock:
            await self._start_unlocked()

    async def _start_unlocked(self) -> None:
        """Internal start logic (caller must hold ``self._lock``)."""
        logger.info(
            "Starting ACP subprocess: %s acp (cwd=%s)",
            self._kiro_cli_path,
            self._cwd,
        )

        self._process = await asyncio.create_subprocess_exec(
            self._kiro_cli_path,
            "acp",
            "-a",
            *(["--model", self._model] if self._model else []),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            cwd=self._cwd,
            limit=10 * 1024 * 1024,  # 10MB buffer for large JSON lines
        )

        assert self._process.stdin is not None
        assert self._process.stdout is not None

        self._reader = ACPReader(self._process.stdout)
        self._writer = JSONRPCWriter(self._process.stdin)

        # Share stdin writer and write lock between reader and writer
        self._reader._stdin_writer = self._process.stdin
        self._reader._write_lock = self._writer._lock

        # Start the background read loop
        self._reader.start()

        # Perform the initialize handshake
        request_id = await self._writer.send_request(
            "initialize",
            {
                "protocolVersion": 1,
                "clientCapabilities": {},
                "clientInfo": {"name": "acp-openai-bridge", "version": "1.0.0"},
            },
        )

        future = self._reader.register_request(request_id)
        response = await future

        if "error" in response:
            logger.error("Initialize handshake failed: %s", response["error"])
            await self._shutdown_unlocked()
            raise RuntimeError(
                f"ACP initialize handshake failed: {response['error']}"
            )

        logger.info("ACP subprocess initialized successfully")
        self._is_available = True

    async def shutdown(self) -> None:
        """优雅关闭子进程，释放管道资源。

        Steps:
        1. Stop the :class:`ACPReader` background task.
        2. Terminate the subprocess.
        3. Wait for the subprocess to exit.

        The entire operation is protected by ``self._lock``.
        """
        async with self._lock:
            await self._shutdown_unlocked()

    async def _shutdown_unlocked(self) -> None:
        """Internal shutdown logic (caller must hold ``self._lock``)."""
        self._is_available = False

        # Stop the reader first
        if self._reader is not None:
            await self._reader.stop()
            self._reader = None

        # Terminate the subprocess
        if self._process is not None:
            try:
                self._process.terminate()
                await asyncio.wait_for(self._process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("ACP subprocess did not exit in time, killing")
                self._process.kill()
                await self._process.wait()
            except ProcessLookupError:
                # Process already exited
                pass
            self._process = None

        self._writer = None
        logger.info("ACP subprocess shut down")

    async def ensure_available(self) -> None:
        """确保子进程可用，如已崩溃则自动重启。

        Checks whether the subprocess is still alive. If it has exited
        or was never started, performs a full restart including the
        ``initialize`` handshake.
        """
        if self._is_available and self._process is not None:
            # Check if the process is still running
            if self._process.returncode is None:
                return
            # Process has exited unexpectedly
            logger.warning(
                "ACP subprocess exited unexpectedly (returncode=%s), restarting",
                self._process.returncode,
            )

        async with self._lock:
            # Double-check under lock
            if self._is_available and self._process is not None and self._process.returncode is None:
                return

            # Clean up any stale state
            await self._shutdown_unlocked()
            # Restart
            await self._start_unlocked()

    @property
    def reader(self) -> ACPReader:
        """Return the :class:`ACPReader` for the current subprocess.

        Raises:
            RuntimeError: If the subprocess is not available.
        """
        if self._reader is None:
            raise RuntimeError("ACP subprocess is not available")
        return self._reader

    @property
    def writer(self) -> JSONRPCWriter:
        """Return the :class:`JSONRPCWriter` for the current subprocess.

        Raises:
            RuntimeError: If the subprocess is not available.
        """
        if self._writer is None:
            raise RuntimeError("ACP subprocess is not available")
        return self._writer

    @property
    def is_available(self) -> bool:
        """Whether the ACP subprocess is running and initialized."""
        return self._is_available
