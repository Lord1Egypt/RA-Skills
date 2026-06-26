#!/bin/bash
cd /Users/robiluo/aicoding/mowenskill
python3 -m pytest tests/test_publish_note.py -v 2>&1 || python3 -m unittest tests.test_publish_note -v 2>&1
