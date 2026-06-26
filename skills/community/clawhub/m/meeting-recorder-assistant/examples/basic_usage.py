"""
Basic usage example for Meeting Recorder Assistant
"""

# Example 1: Record and transcribe audio
print("=" * 50)
print("Example 1: Record and Transcribe")
print("=" * 50)

from scripts.meeting_recorder import MeetingRecorder

recorder = MeetingRecorder()

# Note: Uncomment to actually record
# recorder.start_recording("/tmp/meeting.wav")
# # ... meeting happens ...
# result = recorder.stop_and_transcribe()
# print(f"Transcript: {result['text']}")

print("Note: Recording requires microphone access")
print("Alternative: Transcribe from microphone for short duration")
# result = recorder.transcribe_from_microphone(duration=10)
print()

# Example 2: Generate meeting minutes
print("=" * 50)
print("Example 2: Generate Meeting Minutes")
print("=" * 50)

from scripts.meeting_minutes import generate_minutes, format_as_markdown

# Create a sample transcript for demonstration
sample_transcript = """
会议日期：2024年1月15日
参会人员：张三、李四、王五

本次会议讨论了产品发布计划和营销策略。张三负责准备产品演示文稿。
李四需要联系媒体进行推广。王五将在下周完成技术文档。

决定：产品发布会定于2月1日举行。
下次会议：1月22日
"""

# Save sample transcript
with open("/tmp/sample_transcript.txt", "w", encoding="utf-8") as f:
    f.write(sample_transcript)

# Generate minutes
minutes = generate_minutes("/tmp/sample_transcript.txt", output_format="markdown")
print("Meeting Minutes Generated:")
print(minutes.get("content", "N/A")[:500] + "...")
print()

# Example 3: Extract action items
print("=" * 50)
print("Example 3: Extract Action Items")
print("=" * 50)

from scripts.action_extractor import extract_actions, format_actions_as_markdown

actions = extract_actions("/tmp/sample_transcript.txt")
print(f"Found {len(actions)} action items:")
for action in actions:
    print(f"- {action.get('task', 'N/A')} (Assignee: {action.get('assignee', 'TBD')})")
print()

print("Markdown format:")
print(format_actions_as_markdown(actions))
