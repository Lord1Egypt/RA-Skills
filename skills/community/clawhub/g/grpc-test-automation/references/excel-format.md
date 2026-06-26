# Excel Report Format

## Report Structure

### Sheet 1: Summary

| Field | Value |
|-------|-------|
| Test Plan | VENC gRPC Test |
| Test Date | 2026-03-30 |
| Test Duration | 00:05:32 |
| Total Cases | 8 |
| Passed | 7 |
| Failed | 1 |
| Pass Rate | 87.5% |

### Sheet 2: Test Results

| Test ID | Interface | Request | Expected | Actual | Status | Time(ms) |
|---------|-----------|---------|----------|--------|--------|----------|
| TC-001 | GetDeviceInfo | {"device_id":"BOARD-001"} | device_id=BOARD-001 | device_id=BOARD-001 | PASSED | 2.94 |
| TC-002 | GetVersion | {} | version=1.2.3 | version=1.2.3 | PASSED | 0.74 |
| TC-003 | StartEncoding | {"channel":0,...} | success=true | success=true | PASSED | 1.52 |
| ... | ... | ... | ... | ... | ... | ... |

### Sheet 3: Performance

| Interface | Samples | Avg(ms) | Min(ms) | Max(ms) | 90% Line | Error% | Throughput |
|-----------|---------|---------|---------|---------|----------|--------|------------|
| GetDeviceInfo | 100 | 2.94 | 1.23 | 8.56 | 5.12 | 0% | 340.14/sec |

### Sheet 4: Error Details

| Test ID | Interface | Error Message | Stack Trace |
|---------|-----------|---------------|-------------|
| TC-007 | StartEncoding | Channel is busy | ... |

## Generation Script

```python
import openpyxl
from datetime import datetime

def generate_report(results, output_file):
    wb = openpyxl.Workbook()
    
    # Sheet 1: Summary
    ws1 = wb.active
    ws1.title = "Summary"
    ws1.append(["Test Plan", "VENC gRPC Test"])
    ws1.append(["Test Date", datetime.now().strftime("%Y-%m-%d")])
    ws1.append(["Total Cases", len(results)])
    ws1.append(["Passed", sum(1 for r in results if r['status'] == 'PASSED')])
    ws1.append(["Failed", sum(1 for r in results if r['status'] == 'FAILED')])
    
    # Sheet 2: Test Results
    ws2 = wb.create_sheet("Test Results")
    ws2.append(["Test ID", "Interface", "Request", "Expected", "Actual", "Status", "Time(ms)"])
    for r in results:
        ws2.append([
            r['test_id'], r['interface'], r['request'], 
            r['expected'], r['actual'], r['status'], r['time_ms']
        ])
    
    wb.save(output_file)
```

## Output Location

Reports saved to: `jmeter/results/report_YYYYMMDD_HHMMSS.xlsx`
