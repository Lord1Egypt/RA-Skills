## Description:

Multilingual Learning Sprint is an adaptive language-learning coach that assesses ability, personalizes 7, 14, or 30 day plans, runs practice and review quizzes, and can guide paid lesson flows through Alipay AI Pay or JD ClawTip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carochen112233-commits](https://clawhub.ai/user/carochen112233-commits)

### License/Terms of Use:

MIT-0

## Use Case:

External learners use this skill to diagnose their current language level, choose content they enjoy, and follow a short measurable sprint with lessons, practice, spaced review, and checkpoints. Developers can also use its payment guidance and scripts to connect paid placement, lesson, or quiz workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid-service scripts can send payment credentials and learner data to an unvalidated or overridden service URL.

Mitigation: Run payment scripts only with a trusted backend, restrict or remove local .env.local overrides, and avoid placing sensitive personal text in learner profiles.

Risk: Order-file handling can access order files outside the intended folder when inputs or local configuration are not trusted.

Mitigation: Use trusted order files, confirm order number, amount, payTo, and successful payment status before fulfillment, and keep order files under the OpenClaw orders directory.

Risk: Production payment integrations may rely on unpinned tooling or incomplete merchant setup.

Mitigation: Pin the Alipay npm package before production use and complete merchant authorization, signing, service registration, HTTPS endpoint setup, and payment verification before launch.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/carochen112233-commits/skills/multilingual-learning-sprint)
- [Alipay AI Pay Integration Notes](artifact/references/alipay-aipay.md)
- [Language Skill Research](artifact/references/research.md)
- [Alipay AI Pay Overview](https://aipay.alipay.com/docs/overview.html)
- [Alipay AI Pay Call-Pay Flow](https://aipay.alipay.com/callpay)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown lesson plans, quizzes, feedback, setup guidance, JSON-like learning state, and shell commands for payment workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local ClawTip order files and call a configured paid language-sprint API when payment fulfillment is requested.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
