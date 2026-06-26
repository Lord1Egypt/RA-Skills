# Job Status Query Skill (job-status)

## Overview

This is an OpenClaw skill for querying HPC/AI computing job status. It accesses a specific API with the provided jobId, retrieves detailed job information, and extracts the key status field.

## Features

- ✅ Query job status by jobId
- ✅ Support multiple output formats (JSON, text, table)
- ✅ Complete error handling and retry mechanism
- ✅ Support timeout settings
- ✅ Detailed logging
- ✅ Configurable parameter validation

## Installation Requirements

### System Requirements
- Python 3.6+ or Bash environment
- Network connectivity (must be able to access `www.aicnic.cn`)

### Dependencies
```bash
# Python dependencies
pip install requests

# Bash dependencies (CentOS/RHEL)
yum install curl jq

# Bash dependencies (Ubuntu/Debian)
apt-get install curl jq
```

## Quick Start

### 1. Install Skill
```bash
# Copy skill directory to OpenClaw skills directory
cp -r job-status ~/.openclaw/skills/
```

### 2. Test Skill
```bash
# Using Python script
python scripts/get_job_status.py --job-id 15000

# Using Bash script
bash scripts/get_job_status.sh -j 15000
```

### 3. Use in OpenClaw
```
User: Query job 15000 status
Assistant: Querying job 15000 status...
Job 15000 Status: COMPLETED
Job completed successfully
End Time: 2024-12-09T09:30:10
```

## Detailed Usage

### Basic Query
```json
{
  "jobId": "15000"
}
```

### Parameterized Query
```json
{
  "jobId": "15000",
  "timeout": 10,
  "verbose": true,
  "format": "json"
}
```

### Command Line Usage
```bash
# Basic query
python scripts/get_job_status.py --job-id 15000

# Verbose output
python scripts/get_job_status.py --job-id 15000 --verbose

# Set timeout
python scripts/get_job_status.py --job-id 15000 --timeout 5
```

## Output Description

### Successful Response
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
  "message": "Job completed successfully",
  "timestamp": "2026-03-19T06:30:00Z"
}
```

### Error Response
```json
{
  "success": false,
  "jobId": "99999",
  "error": "Job not found",
  "message": "Job 99999 query failed: Job not found",
  "timestamp": "2026-03-19T06:30:30Z"
}
```

## Configuration

### Configuration File
Skill configuration is in `config.yaml`, you can modify:

```yaml
api:
  base_url: "http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28"
  timeout: 30  # Request timeout in seconds
  retry_count: 3  # Retry count
  
output:
  format: "json"  # Output format
  verbose: false  # Whether to show detailed information
```

### Environment Variables
```bash
# Set timeout
export JOB_STATUS_TIMEOUT=10

# Set retry count
export JOB_STATUS_RETRY_COUNT=3

# Set verbose mode
export JOB_STATUS_VERBOSE=true
```

## Integration Examples

### Use in Python
```python
from scripts.get_job_status import JobStatusFetcher

fetcher = JobStatusFetcher(timeout=10)
result = fetcher.get_job_status("15000")

if result['success']:
    print(f"Job Status: {result['status']}")
    print(f"Details: {result['message']}")
else:
    print(f"Query Failed: {result['error']}")
```

### Use in Bash Scripts
```bash
#!/bin/bash

# Query job status
result=$(bash scripts/get_job_status.sh -j 15000 -v 2>/dev/null)

# Parse status
status=$(echo "$result" | jq -r '.status')

case "$status" in
    "COMPLETED")
        echo "Job completed"
        ;;
    "RUNNING")
        echo "Job is running"
        ;;
    "FAILED")
        echo "Job failed"
        ;;
    *)
        echo "Job status: $status"
        ;;
esac
```

### Use in Scheduled Tasks
```json
{
  "action": "add",
  "job": {
    "name": "Monitor Important Job",
    "schedule": {
      "kind": "every",
      "everyMs": 30000  # Check every 30 seconds
    },
    "payload": {
      "kind": "agentTurn",
      "message": "Query job 15000 status, notify me if status changes"
    }
  }
}
```

## Common Status Descriptions

| Status | Description | Recommended Action |
|--------|-------------|-------------------|
| PENDING | Job is queued | Wait or adjust priority |
| RUNNING | Job is running | Monitor progress |
| COMPLETED | Job completed successfully | Process result data |
| FAILED | Job execution failed | Check error logs and retry |
| CANCELLED | Job was cancelled | Resubmit job |
| TIMEOUT | Job timed out | Increase time limit or optimize job |

## Troubleshooting

### Common Issues

1. **Network Connection Failed**
   ```
   Error: Network connection failed
   ```
   **Solution**: Check network connection, confirm access to `www.aicnic.cn`

2. **Job Not Found**
   ```
   Error: Job not found
   ```
   **Solution**: Verify job ID is correct, job may have been deleted

3. **API Error**
   ```
   Error: API error: Internal server error
   ```
   **Solution**: Try again later, or contact API provider

4. **JSON Parsing Failed**
   ```
   Error: JSON parsing failed
   ```
   **Solution**: Check API response format, ensure valid JSON is returned

### Debugging Methods

```bash
# Enable verbose logging
python scripts/get_job_status.py --job-id 15000 --verbose

# Direct API test
curl -v "http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28/15000"

# Check network connectivity
ping -c 3 www.aicnic.cn
telnet www.aicnic.cn 80
```

### Log Files
Skill runtime generates log files in current directory:
```
logs/job-status.log
```

## Performance Optimization

### Cache Settings
Enable cache in `config.yaml`:
```yaml
cache:
  enabled: true
  ttl: 300  # Cache for 5 minutes
  max_entries: 1000
```

### Batch Query Optimization
Although skill itself only supports single query, batch queries can be optimized with parallel processing:

```bash
#!/bin/bash

# Parallel query multiple jobs
job_ids=(15000 15001 15002 15003 15004)

for job_id in "${job_ids[@]}"; do
    python scripts/get_job_status.py --job-id "$job_id" &
done

wait
echo "All queries completed"
```

## Security Considerations

1. **Input Validation**: Skill automatically validates jobId format
2. **Timeout Protection**: Prevent long blocking
3. **Error Isolation**: Single job query failure doesn't affect others
4. **Log Sanitization**: Don't record sensitive information

## Extending Development

### Adding New Features
1. **Status Change Notifications**: Send notifications when job status changes
2. **Batch Queries**: Support querying multiple jobs at once
3. **History Records**: Record job status change history
4. **Statistical Analysis**: Calculate job success rate, average runtime, etc.

### Modifying API Endpoint
If need to query other HPC system job status, modify API endpoint:

```yaml
api:
  # Modify to other system's API
  base_url: "http://other-hpc-system.com/api/jobs/{jobId}"
```

## License

This project is open source under MIT License.

## Contribution Guidelines

Welcome to submit Issues and Pull Requests!

1. Fork the project
2. Create feature branch
3. Commit changes
4. Create Pull Request

## Contact Information

If you have questions or suggestions, please:
1. Check [Examples Documentation](examples/usage.md)
2. Submit GitHub Issue
3. Contact maintainer

---

**Happy Using!** 🚀