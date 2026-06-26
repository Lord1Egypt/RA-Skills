# YouTube Research Checklist

## Video Selection Criteria

- [ ] Select 2-4 videos with highest view count relevant to topic
- [ ] Prioritize videos from last 6 months (check upload date)
- [ ] Prefer videos with >10K views (top 20% by engagement)
- [ ] Ensure video content actually matches search intent

## Data Extraction Points

For each selected video, extract:
- [ ] Title (exact, for citation)
- [ ] Channel name + subscriber count
- [ ] View count (exact number if available)
- [ ] Upload date
- [ ] Duration
- [ ] Video URL
- [ ] Key quotes or data points from transcript
- [ ] Timestamps of key moments (if chapters available)

## Transcript Handling

- [ ] Run `yt_dlp_captions.py` with `--whisper-if-missing` flag
- [ ] If captions unavailable, note: "Transcript not available"
- [ ] Extract 3-5 most relevant segments (50-200 chars each)
- [ ] Note speaker/presenter if identifiable

## Citation Format

```
根据YouTube视频《{视频标题}》（{频道名}, {观看次数}次观看, {上传日期}）:
"{关键引述或数据}"
来源: {视频URL}
```

## Cross-Verification

- [ ] Verify key claims against at least 1 additional source
- [ ] Flag any claims that appear unsubstantiated
- [ ] Note consensus vs. disagreement across sources
