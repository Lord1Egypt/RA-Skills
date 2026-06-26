import logging
from typing import Optional


def setup_logging(level: int = logging.INFO, formatter: Optional[str] = None) -> None:
    """
    Initialize project-wide logging configuration.

    Args:
        level: Logging level, default INFO.
        formatter: Optional logging format string.
    """
    if not formatter:
        formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    root_logger = logging.getLogger()
    if root_logger.handlers:
        # Update existing handler levels/format to keep configuration consistent.
        for handler in root_logger.handlers:
            handler.setLevel(level)
            handler.setFormatter(logging.Formatter(formatter, '%Y-%m-%d %H:%M:%S'))
        root_logger.setLevel(level)
        return

    logging.basicConfig(
        level=level,
        format=formatter,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
