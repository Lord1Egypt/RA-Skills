# Remote And Hybrid — Rooms, Timezones, Chat And Recording

**Before designing or running a distributed meeting**, read `## Meeting Norms` in `~/Clawic/data/meetings/memory.md` (timezone spread, the overlap window, which slot rotates, who never joins live), `platform.timezone` and `recording_consent` in `config.yaml`, and the attendees' `Context` in `~/Clawic/data/contacts/contacts.md` — who only contributes in chat is a durable fact about a person, not a mood.

**Contents:** [The Hybrid Penalty](#the-hybrid-penalty) · [One Person, One Screen](#one-person-one-screen) · [Chat As A First-Class Channel](#chat-as-a-first-class-channel) · [Running The Remote Room](#running-the-remote-room) · [Timezone Math](#timezone-math) · [Rotating The Painful Slot](#rotating-the-painful-slot) · [Async Instead](#async-instead) · [Recording And Consent](#recording-and-consent) · [Room Setup](#room-setup)

## The Hybrid Penalty

A meeting with six people in a conference room and three on a screen is not one meeting; it is a meeting with an audience. The mechanism is concrete, not cultural:

- **Room audio flattens everyone into one distant voice**, so remote attendees cannot tell who is speaking and lose the half-second cue that opens a turn.
- **Side conversations, whiteboards and eye contact are invisible to the screen.** Half the decision-relevant signal never crosses.
- **Turn-taking runs on micro-cues that a video delay destroys.** A remote participant who tries to interject lands on top of someone and stops trying after the second collision.
- **The room forms a consensus and the screen ratifies it.** By the time the remote attendees are asked, disagreeing means reopening something the room experienced as settled.

The fix is structural. Either everyone is remote, or the meeting is designed so that being in the room confers no advantage.

## One Person, One Screen

The default for any meeting with even one remote attendee: **everyone joins from their own device, with their own camera and microphone, even the people sitting in the same building.**

- **Equal squares on a grid** is the whole point — it restores the visual turn-taking cues and removes the room-versus-screen asymmetry.
- **Headphones for everyone co-located**, or the echo forces the room back onto one microphone. Different rooms if the building allows it.
- **If a shared room is unavoidable**, appoint a named remote advocate in the room whose explicit job is to bring the screen in, and run every round by name so nobody has to fight for a turn.
- **Screens and whiteboards go into the shared document**, always. A physical whiteboard in a hybrid meeting is a decision made in a room half the attendees cannot enter.
- **The chair joins remotely** when most attendees are remote. Whoever holds the room's attention sets the meeting's centre of gravity.

## Chat As A First-Class Channel

- **Name a chat monitor at the top**, out loud, and never the chair. Unmonitored chat is where the best objection of the meeting is posted and never read.
- **Read chat contributions aloud with attribution**: "Lena is asking whether the DPA blocks this." An unspoken chat message did not happen.
- **Chat is the low-friction path for the quiet half of the room.** Some people will type an objection they would never voice; that is a feature to design around, not a habit to correct.
- **Copy anything decision-relevant from chat into the record.** Chat history is not searchable to anyone who was not there, and in most tools it does not survive the meeting.
- **Reactions are a legitimate voting channel** for cheap reversible calls — faster than a round and it captures everyone at once.

## Running The Remote Room

- **Written-first rounds work better remotely than in person.** Two minutes of silent typing into the shared doc gives independent positions and removes the audio collision entirely; it is the single highest-leverage move in a distributed meeting.
- **Call on people by name, always.** "Any thoughts?" produces silence on video, where nobody can read who is about to speak.
- **Hold silence to about seven seconds.** The video delay eats the first two, so the instinct to rescue a pause cuts remote participants off before they have physically begun.
- **Shorter than in person.** 25 and 50 minutes are already the defaults; on video, attention degrades faster and the close needs to arrive earlier, not later.
- **The shared document is the meeting.** Agenda, notes, decisions and actions in one live doc that everyone can see and edit turns a video call into a working session and produces the record for free.
- **Cameras on for 1-on-1s, first meetings and conflict; optional for recurring internal syncs** — the honest trade is trust against fatigue and bandwidth, and it should be a stated norm rather than a per-meeting guess.
- **Say people's names before addressing them**, not after. On a delay, the name is the only cue that a question is aimed at someone.
- **Confirm decisions in text as they happen.** "Decision: CDN stays until Q4, Priya's call" typed into the doc while it is fresh prevents the two-people-heard-different-sentences failure, which is worse on video than in person.

## Timezone Math

- **Compute the actual overlap before proposing anything.** Madrid to San Francisco is 9 hours: the only civilized overlap is roughly 17:00-18:00 CET / 08:00-09:00 PT, which is one hour, and it is the hour everyone wants.
- **Above ~6 hours of spread, a fully-live recurring meeting is a tax on one side forever.** Either it rotates, or it goes async.
- **Above ~9 hours there is no fair slot.** Design the work so the meeting is not required: written decisions with a deadline and a default, plus a recorded update (`meeting-load.md`).
- **Always write times with the zone and the date**, in the recipient's zone: "Tue 30 Jul, 17:00 CET / 08:00 PT". Never "5pm my time".
- **Check the DST gap.** Europe and the US shift on different dates, so a fixed overlap silently moves by an hour twice a year and someone spends two weeks joining at the wrong time.
- **Protect the edges.** A meeting at 08:00 or 19:00 local is at the boundary of someone's day; it is where caregivers and commuters quietly disappear from the room.

## Rotating The Painful Slot

- **Rotate on a fixed schedule, monthly or quarterly**, and announce the schedule rather than negotiating each time. Ad-hoc fairness always resolves in favour of whoever is most senior or most willing to complain.
- **The rotation is a durable norm, not a note in an invite.** Write it into `## Meeting Norms` in `~/Clawic/data/meetings/memory.md` and the series row in `## Series`, so it survives the person who arranged it.
- **Alternate, do not average.** A slot that is uncomfortable for everyone is worse than one that is bad for one region this quarter and another region next quarter.
- **Some meetings should never rotate** — a 1-on-1 with a single remote report is arranged for them, permanently.
- **When a region is permanently on the wrong side of the clock**, the meeting is the wrong tool. Record it, publish the decisions with an objection deadline, and hold a real slot for that region monthly.

## Recording And Consent

Governed by `recording_consent` (`ask` · `announce` · `team-default-ok`), default `ask`.

- **Legal ground varies and the host's consent is not always enough.** Several US states require all-party consent for recording a conversation, and in the EU a recording of identifiable people is personal data that needs a lawful basis and a retention period. Ask; do not assume the platform's button settles it.
- **Announce it verbally at the start, every time**, even where a banner appears. "This is being recorded, it goes to the team channel, and it is deleted after 30 days."
- **Never record a 1-on-1, a performance conversation, a personnel discussion or a legal one.** Recording measurably flattens candour precisely where candour is the entire point.
- **A recording is not a record.** Nobody rewatches an hour; the recap with decisions and owners is what people read. Recording *instead of* deciding is a documented failure mode.
- **Say the retention period out loud and honour it.** An indefinite archive of meetings is a discovery liability and a chilling effect at the same time.
- **Transcripts follow the same rules and are denser in secrets** — passcodes, dial-in PINs and passwords read aloud land in them verbatim (`recaps-and-minutes.md`).
- **Anyone can ask for the recording to stop**, and the request itself is not recorded or noted.

## Room Setup

Tool-agnostic; every platform has these controls under a different name.

- **Test audio, not video.** Bad video is tolerable for an hour; bad audio ends contribution within ten minutes.
- **Wired or headset microphone over laptop built-ins**, and a light source in front of the face rather than behind it.
- **Join two minutes early** with the shared document already open and the screen share tested. The first three minutes of a video meeting are the most commonly wasted block in the working week.
- **A named backup channel** for when the platform fails — the group chat, or a phone bridge — decided in advance, because deciding it during the outage costs the meeting.
- **Join links carrying an embedded passcode, dial-in PINs and meeting passwords are credentials.** They are never written under `~/Clawic/data/`; store the pointer and strip the value (`keychain:standup-dial-in`, `1password:Work/Zoom/board`).

**Write in the same turn as the meeting**: the record block in `~/Clawic/data/meetings/records/<year>-<mm>.md`, decisions in `~/Clawic/data/meetings/decisions.md`, actions in `## Follow-Ups`, and the durable distributed facts — timezone spread, the agreed overlap window, the rotation schedule and who owns which slot, camera and recording norms, the backup channel — into `## Meeting Norms`, with the rotation also reflected in the series row of `## Series` and its next change date in `## Due` (`memory-template.md`). A person who only ever contributes in chat gets that noted in their `Context` in `~/Clawic/data/contacts/contacts.md`, because the fix is to ask them by name next time. A rotation that lives only in an invite reverts to the organizer's timezone within two months.
