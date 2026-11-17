## Description:

Контроль, распознавание и подтверждённая передача показаний водосчётчиков МосОблЕИРЦ по фото через настроенный transport. Используй локальную историю и безопасную отправку только после явного подтверждения владельца.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rommm13](https://clawhub.ai/user/rommm13)

### License/Terms of Use:

MIT No Attribution

## Use Case:

OpenClaw users who manage household water meters registered with MosOblEIRTs use this skill to read photographed meter displays, track local readings, and submit readings through a configured transport after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated provider requests could expose a token if redirected to another origin.

Mitigation: Use only the configured trusted HTTPS provider origin and keep provider credentials in protected secret storage; review the transport before enabling live access.

Risk: A reading could be submitted without the owner's intended approval if the confirmation workflow is not followed.

Mitigation: Require a separate, explicit owner instruction before live submission and treat a reading as verified only after matching provider read-back.

Risk: A reference photo could be overwritten or associated with the wrong meter.

Mitigation: Add reference photos only after an exact serial match or explicit owner confirmation, and associate them with that confirmed meter.

## Reference(s):

- [MosOblEIRC ClawHub release](https://clawhub.ai/rommm13/skills/mosobleirc)
- [MosOblEIRTs account portal](https://lkk.mosobleirc.ru)
- [Yandex Cloud relay documentation](artifact/relay/yandex/README.md)
- [Security guidance](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands]

**Output Format:** [Conversational text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a meter reading summary and a confirmation request before a live submission.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
