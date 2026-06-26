# mfds-cli

Korean **Ministry of Food and Drug Safety (식품의약품안전처)** public-API CLI for AI agents.

Four MFDS Open APIs published on data.go.kr, normalized into clean JSONL:

| Command | Korean | What it returns |
|---|---|---|
| `mfds-cli drug` | 의약품 허가정보 | Drug master — 품목명, 제조사, 주성분, 허가번호, ATC code |
| `mfds-cli drug-easy` | e약은요 | Consumer leaflet — 효능, 용법, 주의, 부작용, 보관 |
| `mfds-cli dur` | DUR 점검정보 | Contraindications + warnings (8 sub-types) |
| `mfds-cli recall` | 의약품 회수/판매중지 | Recalls, sales-stop, disposal orders |

See [`SKILL.md`](./SKILL.md) for the full reference.

## Install

Via the [ClawHub CLI](https://clawhub.ai):

```bash
clawhub install chloepark85/mfds-cli
```

Or clone:

```bash
git clone https://github.com/ChloePark85/mfds-cli.git
chmod +x mfds-cli/bin/*.sh mfds-cli/bin/mfds-cli
```

## Auth

1. Sign up at https://www.data.go.kr (free).
2. 활용신청 each of the four services (instant approval, 10,000 req/day each).
3. Copy the **decoded** serviceKey and:

```bash
export MFDS_API_KEY="<key>"
```

## License

MIT-0. Underlying data: 공공누리 제1유형 — credit "식품의약품안전처".
