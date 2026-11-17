## Description:

免税事業者など登録番号のない相手からの仕入れを課税仕入れの日付で区分し、日本のインボイス経過措置に基づく仕入税額控除額と帳簿記載を案内します。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmshinhwa](https://clawhub.ai/user/jmshinhwa)

### License/Terms of Use:

MIT-0

## Use Case:

一般課税の個人事業主や法人が、免税事業者などからの仕入れを取引ごとに区分し、控除額・控除できない額と帳簿への記載内容を確認するために使用します。

### Deployment Geography for Use:

Japan

## Known Risks and Mitigations:

Risk: Incorrect transaction details or tax treatment could produce an inaccurate deduction amount or misleading filing guidance.

Mitigation: Share only the purchase details needed for calculation and confirm the tax treatment with a tax professional or the tax authority before filing.

Risk: The linked external app's privacy practices were not assessed, so uploading business records there may expose sensitive information.

Mitigation: Assess the external app's privacy practices separately before uploading business records.

## Reference(s):

- [National Tax Agency Q&A 113-3](https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/pdf/qa/113-3.pdf)
- [Invoice transition-measure calculator and ledger app](https://getreadystack.com/ja/apps/invoice-keikasochi-70-shiire-chobo/)
- [ClawHub skill release](https://clawhub.ai/jmshinhwa/skills/invoice-keikasochi-70)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tables and ready-to-use ledger-entry text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calculations use transaction details supplied by the user; confirm tax treatment before filing.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
