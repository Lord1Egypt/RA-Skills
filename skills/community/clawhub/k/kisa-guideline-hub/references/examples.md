# Example Guideline Publications

## Example 1: KISA Guideline

**Source**: KISA (한국인터넷진흥원)
**Title**: "2025년 클라우드 보안 가이드라인"
**Category**: "KISA 가이드라인"
**URL**: https://인터넷진흥원.한국/2060207?page=1
**Date**: 2025-03-09

### Notion Page Structure

```
제목: 2025년 클라우드 보안 가이드라인
카테고리: KISA 가이드라인
날짜: 2025-03-09
URL: https://인터넷진흥원.한국/2060207?page=1

내용:
클라우드 환경에서의 보안 모범 사례를 다룬 가이드라인입니다...
```

### Publishing Command

```bash
cd ~/.openclaw/workspace/skills/security-news-module
python3 ../guideline-publisher/scripts/publish_guidelines.py --full
```

### Expected Output

```
GUIDELINE PUBLISHER
======================================================================

🔄 가이드라인 수집 시작...

KISA...
  ✅ 수집: 1개

📊 총 수집: 1개 가이드라인

🔄 Notion 발행 시작... (1개)

[1/1] 2025년 클라우드 보안 가이드라인...
  ✅ 발행 성공

======================================================================
발행 완료
======================================================================
✅ 성공: 1개
❌ 실패: 0개
📊 성공률: 100.0%
```

---

## Example 2: Boho Guideline (with PDF)

**Source**: Boho (보호나라/KRCERT)
**Title**: "해킹진단도구 활용 방안#5"
**Category**: "보호나라 가이드라인"
**URL**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&nttId=xxx
**Date**: 2025-03-09
**Files**: 해킹진단도구_활용방안5.pdf

### Notion Page Structure

```
제목: 해킹진단도구 활용 방안#5
카테고리: 보호나라 가이드라인
날짜: 2025-03-09
URL: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&nttId=xxx

파일:
📎 해킹진단도구_활용방안5.pdf (다운로드 가능)
```

### PDF Download Process

1. Crawler finds PDF link
2. Downloads to `temp_downloads_boho/해킹진단도구_활용방안5.pdf`
3. Uploads to Notion via file upload API
4. Creates file block in page

---

## Example 3: Multiple Guidelines

**Batch publishing**:

```bash
python3 ../guideline-publisher/scripts/publish_guidelines.py --full
```

### Output

```
KISA...
  ✅ 수집: 10개

Boho...
  ✅ 수집: 11개

📊 총 수집: 21개 가이드라인

🔄 Notion 발행 시작... (21개)

[1/21] 2025년 사이버 위협 대응 가이드라인...
  ✅ 발행 성공

[2/21] 클라우드 보안 구축 가이드...
  ✅ 발행 성공

[3/21] 해킹진단도구 활용 방안#5...
  ✅ 발행 성공 (PDF: 1개)

...

======================================================================
발행 완료
======================================================================
✅ 성공: 21개
❌ 실패: 0개
📊 성공률: 100.0%
```

---

## Common Scenarios

### Scenario 1: First Run

```bash
# No guidelines collected yet
python3 ../guideline-publisher/scripts/publish_guidelines.py --full

# Result: 21 new guidelines published
```

### Scenario 2: Duplicate Prevention

```bash
# Run again immediately
python3 ../guideline-publisher/scripts/publish_guidelines.py --full

# Result: 0 new guidelines (all duplicates)
# KISA...
#   ✅ 수집: 10개 (all duplicates)
# Boho...
#   ✅ 수집: 11개 (all duplicates)
```

### Scenario 3: New Guidelines Available

```bash
# After 1 week, new guidelines published
python3 ../guideline-publisher/scripts/publish_guidelines.py --full

# Result: 3 new guidelines published
# KISA...
#   ✅ 수집: 2개 (new)
# Boho...
#   ✅ 수집: 1개 (new)
```

---

## Troubleshooting Examples

### Error: Database Not Found

```
❌ Error: Notion database not found
```

**Solution**:
```bash
# Check .env file
grep SECURITY_GUIDE_DATABASE_ID ~/.openclaw/workspace/.env

# Or use default
export SECURITY_GUIDE_DATABASE_ID=$SECURITY_NEWS_DATABASE_ID
```

### Error: PDF Upload Failed

```
[5/21] 해킹진단도구 활용 방안#5...
  ❌ Error: File size exceeds limit
```

**Solution**:
- Notion file upload limit: 20MB
- Split large PDFs or compress them

### Error: Network Timeout

```
KISA...
  ❌ Error: HTTPSConnectionPool timeout
```

**Solution**:
- Check network connectivity
- Retry command
- Check firewall settings

---

## Integration with Cron

### LaunchAgent Configuration

```xml
<!-- ~/Library/LaunchAgents/com.openclaw.guidelines.plist -->
<key>ProgramArguments</key>
<array>
    <string>/usr/bin/python3</string>
    <string>/Users/rebugui/.openclaw/workspace/skills/guideline-publisher/scripts/publish_guidelines.py</string>
    <string>--full</string>
</array>
<key>StartInterval</key>
<integer>86400</integer> <!-- Daily -->
```

### Manual Cron

```bash
# Run daily at 9 AM
0 9 * * * cd ~/.openclaw/workspace/skills/security-news-module && python3 ../guideline-publisher/scripts/publish_guidelines.py --full
```
