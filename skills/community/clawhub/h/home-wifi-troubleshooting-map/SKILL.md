---
name: home-wifi-troubleshooting-map
displayName: "Home Wi-Fi Troubleshooting Map"
version: "1.0.1"
description: "Create a safe visible-diagnostic map for home Wi-Fi problems using device symptoms, router lights, placement notes, outage checks, speed tests, and support-ready evidence."
triggerKeywords:
  - home Wi-Fi troubleshooting
  - wifi not working
  - slow wifi map
  - router lights checklist
  - internet outage check
  - home network diagnostic sheet
  - wifi support call prep
tags:
  - home-admin
  - internet
  - wifi
  - troubleshooting
  - support-prep
license: "MIT-0"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Home Wi-Fi Troubleshooting Map

## Purpose

Use this prompt-only skill to help a user organize safe, visible observations for home Wi-Fi or internet trouble. The deliverable is a diagnostic sheet that maps symptoms, affected devices, rooms, router or modem lights, outage checks, basic restart steps if appropriate, speed-test notes, placement issues, and support-call evidence.

This skill is for documentation and low-risk visible checks only. It does not instruct router disassembly, electrical work, cable rewiring inside walls, firmware flashing, credential sharing, or bypassing provider equipment restrictions.

## Use This Skill When

Use this skill when the user reports:

- Wi-Fi is down, slow, intermittent, weak in some rooms, or unstable during calls or streaming.
- One device works but another does not.
- Router, modem, mesh node, or gateway lights changed.
- The user needs to prepare for an ISP, landlord, building network, or device support call.
- The user wants to decide whether the issue looks like device-specific, Wi-Fi coverage, router or modem, ISP outage, or account/service problem.

Do not use it for enterprise network administration, hacking, bypassing parental controls, recovering passwords, opening hardware, or unsafe electrical repairs.

## Best Inputs

Ask for practical details the user can observe safely:

- Internet provider and plan type if known.
- Modem, router, gateway, mesh, or extender model names if visible.
- What changed before the problem started: move, outage, storm, bill issue, new device, update, construction, or new router.
- Affected devices, rooms, apps, and times of day.
- Whether wired Ethernet works, if safely available.
- Router or modem light labels and colors as seen from outside the device.
- Speed-test results, error messages, and outage notices if already available.
- Any safe steps already tried, such as app status check, moving closer, reconnecting Wi-Fi, or a normal power restart.

Do not ask for Wi-Fi passwords, router admin passwords, account passwords, one-time codes, payment details, or private network keys in chat.

## Workflow

1. **Capture the symptom.** Record what fails, when it started, affected devices, affected rooms, and whether the issue is total outage, slow speed, drops, weak coverage, or one-device failure.
2. **Map scope.** Compare device, room, wired, Wi-Fi, and app behavior to classify the likely area: device, Wi-Fi coverage, local router or modem, ISP, building network, or account issue.
3. **Collect visible device status.** Log modem, router, gateway, mesh, or extender light labels and colors exactly as the user sees them. Avoid opening equipment.
4. **Check official channels.** Ask the user to check the ISP app, official outage page, building notices, or support line using trusted contact paths.
5. **List safe visible checks.** Suggest low-risk checks such as confirming power indicator, checking that cables are seated from the outside, moving closer, testing another device, checking airplane mode, or running a speed test.
6. **Document restart history.** If the user chooses to restart equipment, record what was restarted, how long it was unplugged, and what changed. Do not pressure the user to unplug equipment in unsafe conditions.
7. **Identify escalation triggers.** Flag signs that support, landlord, electrician, or emergency help may be needed, such as damaged power cords, burning smell, sparks, exposed wiring, water near equipment, repeated breaker trips, or provider outage.
8. **Prepare the support script.** Summarize observations, tests, light status, impact, account-safe identifiers, and questions for ISP or device support.

## Output Format

Return a visible-diagnostic sheet in this order:

1. **Current Situation**

| Field | Detail |
|---|---|
| Main problem | |
| Started | |
| Affected devices | |
| Affected rooms | |
| Works anywhere? | |
| Recent change | |
| Safety concern | |

2. **Scope Map**

| Test or observation | Result | What it suggests | Follow-up |
|---|---|---|---|
| Same device near router | | | |
| Different device same room | | | |
| Different room | | | |
| Wired Ethernet, if safely available | | | |
| ISP app or outage page | | | |
| Speed test | | | |

3. **Visible Equipment Status**

| Device | Location | Light label | Light color or pattern | Notes |
|---|---|---|---|---|

4. **Safe Checks Already Tried**

| Check | Result | Time | Notes |
|---|---|---|---|

Include only external, visible, low-risk checks.

5. **Likely Issue Area**

Rank these categories with confidence and reason:

- Device-specific
- Wi-Fi coverage or interference
- Router, gateway, mesh, or extender
- Modem or provider line
- ISP or building outage
- Account, billing, or service provisioning
- Unknown

6. **Support Call Script**

Provide a short script with the problem, start time, affected devices and rooms, visible light status, outage-check result, safe checks tried, impact, and exact questions for support. Include a request for a case number and written summary.

7. **Next Actions**

| Priority | Action | Owner | Safe to do now? | Notes |
|---|---|---|---|---|

8. **Do Not Do List**

List unsafe or out-of-scope actions to avoid, tailored to the case.

## Style Rules

- Keep advice practical, calm, and non-technical unless the user provides technical details.
- Use exact user wording for light colors, error messages, and room names.
- Separate observations from conclusions.
- Prefer official provider instructions for device-specific restart, reset, account, or outage steps.
- Mark unknown details rather than guessing.

## Safety Boundary

- Do not instruct the user to open routers, modems, mesh nodes, wall plates, electrical panels, outlets, or provider-owned boxes.
- Do not instruct cutting, splicing, rewiring, soldering, bypassing, drilling, ladder work, roof work, or attic/crawlspace cable work.
- Do not ask for Wi-Fi passwords, router admin passwords, ISP account passwords, one-time codes, payment details, MAC address screenshots with personal labels, or private security settings in chat.
- Do not recommend factory reset, firmware flashing, advanced admin changes, DNS changes, bridge mode, port forwarding, or disabling security unless the user explicitly asks and understands the risks.
- If there is smoke, burning smell, sparks, exposed wiring, water near powered equipment, electric shock, fire risk, damaged power supply, or repeated breaker trip, stop routine troubleshooting and direct the user to avoid the area if needed and contact emergency services, the utility provider, landlord, building management, ISP, or a qualified professional as appropriate.

## Example Prompts

- "My home Wi-Fi keeps dropping. Make a troubleshooting map."
- "Only the bedroom has bad Wi-Fi. Help me collect evidence before calling support."
- "The router light is red and my laptop cannot connect. What should I check safely?"
- "Build a support call script for my ISP from these symptoms."
