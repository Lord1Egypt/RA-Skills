---
name: meeting-os
description: Auto meeting notes and action item execution loop. Trigger this skill whenever the user mentions meeting notes, meeting summary, action items, follow-up, transcript, recording, Zoom summary, Teams meeting, Tencent Meeting, Feishu meeting, WeCom meeting, upload audio, upload video, meeting template, task creation.
license: MIT
user-invocable: true
argument-hint: Free: 10 meetings/month. Pro billing via SkillPay: skillpay.me
---

# MeetingOS

Auto meeting notes and action item execution loop.

## Required Environment Variables

This skill uses the following environment variables.
You must set them yourself in a local .env file.
Never upload your .env file to any website.

The following variables control basic behavior and have safe defaults:

- MEETINGOS_PRIVACY_MODE: Set to local or cloud. Default is local. Local mode keeps all data on your computer.
- WHISPER_LOCAL_MODEL: Set to base or medium or large-v3. Default is base.
- MEETINGOS_DOWNLOAD_DIR: Folder for temporary recording files. Default is /tmp/meetingos.
- MEETINGOS_MAX_FILE_MB: Maximum file size in MB. Default is 2048.

The following variables are needed only if you use Feishu integration:

- FEISHU_APP_ID: Your Feishu App ID. Get from open.feishu.cn
- FEISHU_APP_SECRET: Your Feishu App Secret. Get from open.feishu.cn
- FEISHU_CHAT_ID: Your Feishu group chat ID. Get from Feishu group settings.
- FEISHU_WEBHOOK_URL: Your Feishu robot Webhook URL. Get from Feishu group robot settings.
- FEISHU_BITABLE_TOKEN: Your Feishu Bitable App Token. Get from the Bitable URL.
- FEISHU_BITABLE_TABLE: Your Feishu Bitable Table ID. Get from the Bitable URL.

The following variables are needed only if you use WeCom integration:

- WECOM_CORP_ID: Your WeCom Corp ID. Get from WeCom admin panel.
- WECOM_AGENT_ID: Your WeCom Agent ID. Get from WeCom admin panel.
- WECOM_AGENT_SECRET: Your WeCom Agent Secret. Get from WeCom admin panel.
- WECOM_WEBHOOK_URL: Your WeCom robot Webhook URL. Get from WeCom group robot settings.

The following variables are needed only if you use Notion integration:

- NOTION_API_KEY: Your Notion Integration Token. Get from notion.so/my-integrations
- NOTION_DATABASE_ID: Your Notion Database ID. Get from the Notion database page URL.

The following variable is needed only if you want cloud transcription:

- OPENAI_API_KEY: Your OpenAI API Key. Get from platform.openai.com/api-keys. Not needed if you use local mode.

The following variables are needed only if you use SkillPay billing:

- SKILLPAY_API_KEY: Your SkillPay API Key. Get from skillpay.me/dashboard
- SKILLPAY_SKILL_ID: Your SkillPay Skill ID. Get from skillpay.me/dashboard/skills

## Installation

Install Python packages:
```
pip install -r requirements.txt
```

Install ffmpeg for audio processing:

- Windows: download from ffmpeg.org then restart your computer
- Mac: run brew install ffmpeg
- Linux: run sudo apt install ffmpeg

## When to Use

- Help me organize this meeting
- Extract action items from this transcript
- Push action items to Notion or Feishu or WeCom
- Generate meeting notes from this recording
- Follow up on last meeting action items
- Send summary to Feishu group
- Batch process multiple meeting recordings

## Privacy

When MEETINGOS_PRIVACY_MODE is set to local, audio stays on your computer. No data is sent anywhere. This is the default.

When set to cloud, audio is sent to OpenAI. Only use this if you are comfortable with that.

## Security

- All API keys must be stored in your own .env file
- Never upload your .env file to any website
- Never paste real key values into code or documentation files
- Only configure the services you actually plan to use
- Temporary recording files are deleted automatically after processing

## File Structure
```
meeting-os/
├── SKILL.md
├── requirements.txt
├── scripts/
│   ├── transcribe.py
│   ├── push_notion.py
│   ├── feishu_helper.py
│   ├── wecom_helper.py
│   ├── meeting_fetcher.py
│   ├── skillpay_guard.py
│   └── main_processor.py
└── templates/
    ├── default.md
    └── sales_debrief.md
```
```

---

## 第二件事：在 GitHub 提交人工审核申请

因为我们已经修了很多版本，这次修完后同时提交人工审核，让 ClawHub 团队确认。

**操作：**
1. 在技能页面点击黄色警告框里的 **「在 GitHub 上提交交问题」** 链接
2. 跳转到 GitHub 后点击 **「New Issue」**
3. 标题填：
```
MeetingOS skill flagged as suspicious - all issues fixed, requesting manual review
```

4. 内容填：
```
Hello,

I have fixed all flagged issues in version 1.0.6. Here is what was fixed:

1. Removed all real API key values from all files
2. Added complete environment variable documentation to SKILL.md
3. All environment variables used in code are now declared in SKILL.md
4. Added requirements.txt with all Python dependencies
5. All test code is inside if __name__ == "__main__" blocks
6. No .env file is included in the upload

The skill is a meeting notes automation tool that:
- Transcribes audio using local Whisper (no data sent anywhere by default)
- Extracts action items from transcripts
- Optionally pushes to Feishu, WeCom, Notion (only if user configures their own keys)
- Optionally uses SkillPay billing (only if user configures their own keys)

All external service calls are optional and require the user to provide their own credentials.

Please review and remove the suspicious flag.

Account: DTTNpole-commits
Skill: meetingos

Thank you.