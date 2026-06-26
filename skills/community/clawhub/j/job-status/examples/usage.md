# Job Status Query Skill Usage Examples

## Basic Usage

### Example 1: Query Single Job Status

**Input**:
```json
{
  "jobId": "15000"
}
```

**Output**:
```json
{
  "success": true,
  "jobId": "15000",
  "status": "COMPLETED",
  "details": {
    "jobState": "COMPLETED",
    "jobId": "15000",
    "id": 20452,
    "hpcId": "hpcai28",
    "endTime": "2024-12-09T09:30:10"
  },
  "message": "Job completed successfully",
  "timestamp": "2026-03-19T06:30:00Z"
}
```

### Example 2: Query Running Job

**Input**:
```json
{
  "jobId": "15001",
  "verbose": true
}
```

**Output**:
```json
{
  "success": true,
  "jobId": "15001",
  "status": "RUNNING",
  "details": {
    "jobState": "RUNNING",
    "jobId": "15001",
    "id": 20453,
    "hpcId": "hpcai28",
    "startTime": "2024-12-09T09:00:00",
    "runTime": "1800",
    "numNodes": 2,
    "numCPUs": 16
  },
  "message": "Job is currently running",
  "timestamp": "2026-03-19T06:30:10Z"
}
```

### Example 3: Query Failed Job

**Input**:
```json
{
  "jobId": "15002"
}
```

**Output**:
```json
{
  "success": true,
  "jobId": "15002",
  "status": "FAILED",
  "details": {
    "jobState": "FAILED",
    "jobId": "15002",
    "id": 20454,
    "hpcId": "hpcai28",
    "endTime": "2024-12-09T09:15:00",
    "exitCode": 1,
    "exitStatus": "Out of memory"
  },
  "message": "Job execution failed",
  "timestamp": "2026-03-19T06:30:20Z"
}
```

## Advanced Usage

### With Timeout Setting

```json
{
  "jobId": "15000",
  "timeout": 10
}
```

### Concise Output Mode

```json
{
  "jobId": "15000",
  "verbose": false,
  "format": "text"
}
```

Output:
```
Job 15000 Status: COMPLETED
Job completed successfully
End Time: 2024-12-09T09:30:10
```

### Table Format Output

```json
{
  "jobId": "15000",
  "format": "table"
}
```

Output:
```
┌─────────┬────────────┬────────────┬─────────────────────┐
│ Job ID  │   Status   │   HPC ID   │     End Time        │
├─────────┼────────────┼────────────┼─────────────────────┤
│ 15000   │ COMPLETED  │ hpcai28    │ 2024-12-09 09:30:10 │
└─────────┴────────────┴────────────┴─────────────────────┘
```

## Error Handling Examples

### Job Not Found

**Input**:
```json
{
  "jobId": "99999"
}
```

**Output**:
```json
{
  "success": false,
  "jobId": "99999",
  "error": "Job not found",
  "message": "Job 99999 query failed: Job not found",
  "timestamp": "2026-03-19T06:30:30Z"
}
```

### Network Timeout

**Input**:
```json
{
  "jobId": "15000",
  "timeout": 5
}
```

**Output**:
```json
{
  "success": false,
  "jobId": "15000",
  "error": "Request timeout",
  "message": "Job 15000 query failed: Request timeout",
  "timestamp": "2026-03-19T06:30:35Z"
}
```

### Invalid Job ID Format

**Input**:
```json
{
  "jobId": "abc123"
}
```

**Output**:
```json
{
  "success": false,
  "jobId": "abc123",
  "error": "Invalid job ID format",
  "message": "Job ID must be numeric",
  "timestamp": "2026-03-19T06:30:40Z"
}
```

## Integration Examples

### Use in Scripts

```bash
#!/bin/bash

# Query job status
result=$(python scripts/get_job_status.py --job-id 15000 --verbose)

# Parse result
status=$(echo "$result" | jq -r '.status')

if [[ "$status" == "COMPLETED" ]]; then
    echo "Job completed, can proceed with next steps"
elif [[ "$status" == "RUNNING" ]]; then
    echo "Job still running, please wait"
else
    echo "Job status abnormal: $status"
fi
```

### Use in Scheduled Tasks

```json
{
  "action": "add",
  "job": {
    "name": "Monitor Job Status",
    "schedule": {
      "kind": "every",
      "everyMs": 60000  # Check every minute
    },
    "payload": {
      "kind": "agentTurn",
      "message": "Query job 15000 status, notify me if completed"
    }
  }
}
```

## Batch Query Examples

Although the skill itself only supports single job query, batch queries can be achieved through loops:

```bash
#!/bin/bash

# Batch query job status
job_ids=("15000" "15001" "15002" "15003")

for job_id in "${job_ids[@]}"; do
    echo "Querying job $job_id status:"
    python scripts/get_job_status.py --job-id "$job_id"
    echo ""
done
```

Or using parallel processing:

```bash
#!/bin/bash

# Use GNU parallel for parallel queries
parallel -j 4 "python scripts/get_job_status.py --job-id {}" ::: 15000 15001 15002 15003
```

## Job Status Monitoring

```python
#!/usr/bin/env python3
"""
Monitor job status changes
"""

import time
from get_job_status import JobStatusFetcher

def monitor_job_status(job_id, interval=60, max_checks=10):
    """Monitor job status changes"""
    fetcher = JobStatusFetcher()
    previous_status = None
    
    for i in range(max_checks):
        result = fetcher.get_job_status(job_id)
        
        if result['success']:
            current_status = result['status']
            
            if previous_status is None:
                print(f"Initial status: {current_status}")
            elif current_status != previous_status:
                print(f"Status changed: {previous_status} -> {current_status}")
                print(f"Time: {result['timestamp']}")
                
                # If job completed, can trigger follow-up actions
                if current_status == "COMPLETED":
                    print("Job completed, can proceed with next steps")
                    break
            
            previous_status = current_status
        else:
            print(f"Query failed: {result['error']}")
        
        # Wait if not last check
        if i < max_checks - 1:
            time.sleep(interval)
    
    print("Monitoring ended")

if __name__ == "__main__":
    monitor_job_status("15000", interval=30, max_checks=20)
```

## Best Practices

### 1. Parameter Validation
```json
{
  "jobId": "15000",
  "timeout": 10,
  "verbose": false
}
```

### 2. Error Handling
```python
try:
    result = get_job_status(job_id)
    if result['success']:
        # Handle success
    else:
        # Handle error
        log_error(result['error'])
except Exception as e:
    # Handle exception
```

### 3. Performance Optimization
- Enable cache for frequently queried jobs
- Use parallel processing for batch queries
- Set appropriate timeout values

### 4. Monitoring and Alerting
- Set up job completion notifications
- Monitor long-running jobs
- Record job status history

## Troubleshooting

### Common Issues

1. **Network Connection Failed**
   ```
   Error: Network connection failed
   ```
   **Solution**: Check network connectivity, confirm access to www.aicnic.cn

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
# Verbose mode to see request process
python scripts/get_job_status.py --job-id 15000 --verbose

# Direct API test
curl -v "http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28/15000"

# Check network connectivity
ping -c 3 www.aicnic.cn
```

## Log Files

Skill runtime generates log files in current directory:
```
logs/job-status.log
```

We hope these examples help you better use the job status query skill!