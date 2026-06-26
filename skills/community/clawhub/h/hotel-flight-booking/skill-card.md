## Description: <br>
Booking.com国际酒店预订助手，支持全球酒店搜索、房型查询、价格对比、预订管理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-support agents use this skill to search international hotels, compare room availability and prices, and format Booking.com-style hotel information. Reservation claims need review because server security evidence says the artifacts do not show a real booking workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may believe a real booking, cancellation, or reservation lookup was completed when server security evidence says the artifacts do not show a real booking workflow. <br>
Mitigation: Review before installing and require explicit confirmation IDs, cancellation or charge warnings, and verified Booking.com or partner API responses before presenting reservation actions as complete. <br>
Risk: Hotel, price, availability, or review data may be misleading if generated from placeholder or demo behavior instead of live partner data. <br>
Mitigation: Display only data returned by the authorized Booking.com or partner API and label any unavailable live data as unavailable rather than substituting examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-zry/hotel-flight-booking) <br>
- [Booking.com distribution JSON API](https://distribution-xml.booking.com/json) <br>
- [Booking.com getHotels API endpoint](https://distribution-xml.booking.com/json/bookings.getHotels) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, code, guidance] <br>
**Output Format:** [JSON responses and Markdown-formatted hotel or room summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Booking.com API credentials; booking and cancellation outputs should be treated as unverified unless a real reservation workflow is confirmed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
