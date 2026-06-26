import logging
import os
import time
from pathlib import Path

class ImmediateFlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

def setup_orchestrator_logger(workdir, debug_mode):
    log_dir = Path(workdir) / ".tmp" / "sdlc_logs"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        # Cleanup logs older than 7 days
        now = time.time()
        for f in log_dir.glob("orchestrator_*.log"):
            try:
                if f.is_file() and (now - f.stat().st_mtime) > 7 * 86400:
                    f.unlink()
            except Exception:
                pass
    except Exception as e:
        pass

    logger = logging.getLogger("sdlc_orchestrator")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            pid = os.getpid()
            log_file = log_dir / f"orchestrator_{timestamp}_{pid}.log"
            file_handler = ImmediateFlushFileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception:
            pass

        console_handler = logging.StreamHandler()
        console_level = logging.DEBUG if debug_mode else logging.INFO
        console_handler.setLevel(console_level)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger
