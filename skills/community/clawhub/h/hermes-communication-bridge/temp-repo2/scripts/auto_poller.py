#!/usr/bin/env python3
"""自动轮询脚本 - 定期检查来自 Hermes 的消息"""

import sys
import time
import json
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from communication_queue import CommunicationQueue

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

POLL_INTERVAL = 5

def poll_for_messages():
    queue = CommunicationQueue()
    while True:
        messages = queue.get_messages("workbuddy", status="pending")
        for msg in messages:
            logger.info(f"收到来自 {msg['sender']} 的消息: {msg['content'][:50]}...")
            queue.mark_as_processed(msg['id'], status="completed")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    poll_for_messages()
