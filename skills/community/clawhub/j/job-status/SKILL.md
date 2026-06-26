---
name: job-status
description: |
  HPC/AI job status query skill. Fetches job status information by jobId from a specific API endpoint and parses the jobState field from the JSON response.

  **Use this skill when**:
  (1) Need to query HPC/AI computing job status
  (2) User provides a jobId parameter
  (3) Need to get job status (e.g., RUNNING, COMPLETED, FAILED)
  (4) Need to monitor computing job progress
alwaysActive: false
metadata:
  openclaw:
    emoji: "⚡"
    category: "monitoring"
    author: "OpenClaw Assistant"
    version: "1.0.0"
---

# Job Status Query Skill

## 🎯 Function Overview

This skill queries HPC/AI computing job status information. It accesses the API with the provided jobId, retrieves detailed job information, and extracts the key status field.

## 🔧 Technical Implementation

- **API Endpoint**: `http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28/{jobId}`
- **Response Format**: JSON
- **Key Field**: `data.jobState`
- **Error Handling**: Network timeout, API errors, JSON parsing errors

## 📋 Quick Start

### Method 1: Natural Language Call
```
User: Query job status, jobId is 15000
Assistant: Querying job 15000 status...
```

### Method 2: Parameterized Call
```json
{
  "jobId": "15000"
}
```

## 🚀 Usage Scenarios

### Scenario 1: Query Single Job Status
```json
{
  "jobId": "15000"
}
```

### Scenario 2: Batch Job Status Query
User: Query status for jobs 15000, 15001, 15002

### Scenario 3: Monitor Job Completion
User: Check if job 15000 is completed

## 🔍 Return Status Description

Common `jobState` values:
- **PENDING**: Job is queued
- **RUNNING**: Job is running
- **COMPLETED**: Job completed successfully
- **FAILED**: Job execution failed
- **CANCELLED**: Job was cancelled
- **TIMEOUT**: Job timed out

## ⚠️ Notes

1. **jobId Format**: Must be a valid job ID
2. **Network Connectivity**: Must be able to access `www.aicnic.cn`
3. **API Limits**: Be aware of API rate limits
4. **Error Handling**: Network errors or invalid jobId will return appropriate error messages

## 📊 Example Responses

Successful response:
```json
{
  "success": true,
  "jobId": "15000",
  "status": "COMPLETED",
  "details": {
    "jobState": "COMPLETED",
    "endTime": "2024-12-09T09:30:10",
    "id": 20452
  },
  "message": "Job query successful",
  "timestamp": "2026-03-19T06:30:00Z"
}
```

Error response:
```json
{
  "success": false,
  "jobId": "99999",
  "error": "Job not found or access failed",
  "message": "API returned error or network connection failed",
  "timestamp": "2026-03-19T06:30:30Z"
}
```

## 🔗 Related Skills

- **System Monitoring**: Can be combined with system monitoring skills
- **Notification Alerts**: Can trigger notifications on job status changes
- **Log Recording**: Record job status history