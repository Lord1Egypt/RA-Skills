import pytest


@pytest.fixture
def transcript_labeled():
    return """\
Alice: Good morning everyone. Let's start with the budget review.
Bob: Sure. We need to decide on Q3 allocations before end of month.
Alice: Right. My proposal is to increase marketing by 15%.
Bob: I agree with that direction. What about the deadline?
Alice: Let's set August 15 as the final decision point.
Carol: That works for me. I can own the marketing side.
Bob: Great. Moving on — what about the product roadmap?
Alice: We decided last week to prioritize mobile. Still on track.
Carol: Yes. I've already started the design sprint.
Bob: Good. Any blockers?
Carol: Not really, just some minor dependency issues.
Alice: Ok, let's table that for now. Anything else?
Bob: I think we're good. Short meeting today, nice.
Alice: Agreed. Let's reconvene next Tuesday.
Carol: Sounds good. See everyone then.
Alice: Thanks everyone. Budget decision is final — Carol owns it, deadline Aug 15.
"""


@pytest.fixture
def transcript_plain():
    return """\
The meeting opened with a discussion about the current state of the project timeline.
Several participants raised concerns about the delayed delivery of the backend API module.
There was general agreement that the testing phase had been underestimated in the original plan.
The team spent considerable time reviewing the dependency graph for the upcoming release.
One of the main topics was whether to proceed with the current architecture or refactor.
Arguments were made in favor of refactoring to improve long-term maintainability.
Others pointed out that the deadline pressure made refactoring risky at this stage.
The conversation shifted to resource allocation and whether additional engineers were needed.
Budget constraints were acknowledged as a limiting factor in hiring new team members.
The group discussed the possibility of reassigning existing staff from lower-priority tasks.
There was some debate about which tasks could realistically be deprioritized without impact.
Eventually the discussion moved to communication practices between frontend and backend teams.
It was noted that daily standups had been inconsistent over the past two weeks.
Some participants suggested moving to async updates via a shared document instead.
The meeting concluded without formal decisions, but several action items were noted informally.
"""


@pytest.fixture
def transcript_whisperx():
    return """\
[00:00:01.20 --> 00:00:05.80] SPEAKER_01: Welcome everyone. Today we need to finalize the product launch date.
[00:00:06.10 --> 00:00:12.40] SPEAKER_02: I think we should aim for mid-September. That gives us six weeks of buffer.
[00:00:12.80 --> 00:00:18.50] SPEAKER_01: Agreed. Let's lock in September 14th as our target.
[00:00:19.00 --> 00:00:25.30] SPEAKER_03: What about the QA sign-off? We still need two weeks for that.
[00:00:25.70 --> 00:00:31.20] SPEAKER_02: Right, so code freeze should be August 31st at the latest.
[00:00:31.50 --> 00:00:37.00] SPEAKER_01: That works. Who owns the QA coordination?
[00:00:37.40 --> 00:00:43.80] SPEAKER_03: I can take that. I'll set up the test plan by end of this week.
[00:00:44.10 --> 00:00:50.60] SPEAKER_01: Perfect. Let's also confirm the marketing materials deadline.
[00:00:51.00 --> 00:00:57.30] SPEAKER_02: Marketing needs the final feature list by August 20th to hit their deadline.
[00:00:57.70 --> 00:01:03.40] SPEAKER_01: Noted. I'll make sure engineering delivers specs by August 18th.
[00:01:03.80 --> 00:01:10.20] SPEAKER_03: Any concerns about the payment integration? That was flagged last sprint.
[00:01:10.50 --> 00:01:16.80] SPEAKER_02: It's resolved. The third-party SDK update fixed the timeout issue.
[00:01:17.20 --> 00:01:23.50] SPEAKER_01: Great. So decisions: launch September 14, code freeze August 31, QA owned by Speaker 3.
[00:01:23.90 --> 00:01:29.00] SPEAKER_03: Confirmed. I'll send out a summary after this call.
[00:01:29.30 --> 00:01:33.10] SPEAKER_01: Thanks everyone. We're done.
"""


@pytest.fixture
def mock_llm(monkeypatch):
    def fake_chat(self, messages, schema=None):
        content = " ".join(m.get("content", "") for m in messages).lower()
        if "filler" in content or "efficiency" in content:
            return {"filler_windows": [0], "total_windows": 5}
        return [{"topic": "budget", "decided": True, "owner": "Alice", "deadline": "Aug 15"}]

    from scripts import llm_adapter
    monkeypatch.setattr(llm_adapter.LLMClient, "chat", fake_chat)
