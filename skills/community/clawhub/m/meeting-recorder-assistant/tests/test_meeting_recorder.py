"""
Unit tests for Meeting Recorder Assistant
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.meeting_recorder import MeetingRecorder
from scripts.meeting_minutes import (
    generate_minutes,
    extract_attendees,
    extract_action_items,
    extract_decisions,
    format_as_markdown
)
from scripts.action_extractor import extract_actions, export_actions_to_json


class TestMeetingRecorder(unittest.TestCase):
    """Test cases for meeting recorder"""
    
    def test_meeting_recorder_init(self):
        """Test MeetingRecorder initialization"""
        recorder = MeetingRecorder()
        self.assertFalse(recorder.recording)
        self.assertEqual(recorder.rate, 44100)
    
    def test_transcribe_audio_file_not_found(self):
        """Test transcribe with non-existent file"""
        recorder = MeetingRecorder()
        result = recorder.transcribe_audio("/nonexistent/file.wav")
        self.assertEqual(result["status"], "error")


class TestMeetingMinutes(unittest.TestCase):
    """Test cases for meeting minutes generation"""
    
    def test_extract_attendees(self):
        """Test attendee extraction"""
        text = "参会人员：张三、李四、王五\n张三：出席"
        attendees = extract_attendees(text)
        self.assertIn("张三", attendees)
    
    def test_extract_action_items(self):
        """Test action item extraction"""
        text = "张三需要完成报告。李四负责联系客户。"
        actions = extract_action_items(text)
        self.assertTrue(len(actions) > 0)
    
    def test_extract_decisions(self):
        """Test decision extraction"""
        text = "我们决定下周发布产品。同意采用新方案。"
        decisions = extract_decisions(text)
        self.assertTrue(len(decisions) > 0)
    
    def test_format_as_markdown(self):
        """Test markdown formatting"""
        minutes = {
            "meeting_date": "2024-01-15",
            "attendees": ["张三", "李四"],
            "summary": "Test summary",
            "topics_discussed": ["Topic 1", "Topic 2"],
            "decisions_made": ["Decision 1"],
            "action_items": [
                {"task": "Task 1", "assignee": "张三", "due_date": None, "priority": "high"}
            ],
            "next_meeting": "2024-01-22"
        }
        md = format_as_markdown(minutes)
        self.assertIn("Meeting Minutes", md)
        self.assertIn("张三", md)


class TestActionExtractor(unittest.TestCase):
    """Test cases for action item extractor"""
    
    def test_extract_actions_from_text(self):
        """Test action extraction from text"""
        # Create temp file
        with open("/tmp/test_transcript.txt", "w", encoding="utf-8") as f:
            f.write("张三需要完成报告。action item: 联系客户由李四负责。")
        
        actions = extract_actions("/tmp/test_transcript.txt")
        self.assertTrue(len(actions) > 0)
        
        # Cleanup
        os.remove("/tmp/test_transcript.txt")
    
    def test_export_actions_to_json(self):
        """Test JSON export"""
        actions = [{"task": "Test", "assignee": "User"}]
        result = export_actions_to_json(actions, "/tmp/test_actions.json")
        self.assertTrue(result)
        
        # Verify file exists
        self.assertTrue(os.path.exists("/tmp/test_actions.json"))
        
        # Cleanup
        os.remove("/tmp/test_actions.json")


if __name__ == "__main__":
    unittest.main(verbosity=2)
