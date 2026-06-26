# 🧭 Gingiris Growth Finder — AI 성장 전략 라우터

> **제품 유형, 성장 단계, 채널 격차를 진단하고 가장 적합한 Gingiris 플레이북을 자동 추천하는 메타 스킬.** Iris(生姜iris) 제작, Forbes Asia 30 Under 30.

**[English](README.md) | [中文](README_zh.md) | [日本語](README_ja.md) | [한국어](README_ko.md)**

---

## 이게 뭔가요?

성장 관련 질문은 비슷해 보이지만, 실제로는 완전히 다른 플레이북이 필요합니다. "어떻게 런칭하지?"라는 질문은 개발자 도구와 모바일 앱에서 전혀 다른 답을 요구합니다. "어떻게 성장하지?"도 $1M ARR 단계와 100 DAU 단계에서 하늘과 땅 차이입니다.

이 스킬은 세 가지 차원에서 상황을 진단한 후, 적합한 전문 플레이북을 호출합니다:

1. **제품 유형** — SaaS / 오픈소스 / 모바일 앱 / 개발자 도구 / 소비자 웹 / 마켓플레이스
2. **성장 단계** — 프리런칭 / 런칭 / 콜드 스타트 / 그로스 / 스케일
3. **채널 격차** — 콘텐츠 / 커뮤니티 / 유료 광고 / 파트너십 / 프로덕트 레드

## 라우팅 규칙

| 당신의 상황 | 라우팅 대상 |
|---|---|
| Product Hunt 런칭, Hunter 섭외, 런칭 데이 전술 | **[gingiris-launch](https://skills.sh/Gingiris/gingiris-launch)** |
| GitHub Star 성장, HackerNews, OSS GTM | **[gingiris-opensource](https://skills.sh/Gingiris/gingiris-opensource)** |
| B2B SaaS, PLG/SLG, PMF 검증, 엔터프라이즈 성장 | **[gingiris-b2b-growth](https://skills.sh/Gingiris/gingiris-b2b-growth)** |
| ASO, 모바일 UA, TikTok/Reels/Shorts UGC 매트릭스 | **[gingiris-aso-growth](https://skills.sh/Gingiris/gingiris-aso-growth)** |

---

## 활용 예시

```
"다음 주에 AI SaaS 런칭하는데 — 뭘 먼저 해야 하죠?"
"오픈소스 프로젝트가 2k stars인데 10k까지 어떻게 가나요?"
"B2B SaaS $300k ARR 달성했는데, SDR 채용해야 할까요?"
"iOS 앱 메인 키워드 순위가 안 올라가는데 어떻게 하나요?"
"Product Hunt 1위를 노리고 있는데, 어떻게 준비해야 하나요?"
```

스킬은 먼저 진단 결과를 제시하고, 해당 전문 스킬이 로드되지 않은 경우 설치를 제안합니다.

---

## 설치 방법

```bash
npx skills add Gingiris/gingiris-growth-finder -g
```

설치 후 Claude Code, Cursor, Codex, Amp, Cline 등 7+ Agent Skills 런타임에서 자동 로드됩니다.

---

## Gingiris 전체 시리즈 설치

```bash
npx skills add Gingiris/gingiris-growth-finder -g     # 이 메타 라우터
npx skills add Gingiris/gingiris-launch -g            # Product Hunt
npx skills add Gingiris/gingiris-opensource -g        # OSS / GitHub Stars
npx skills add Gingiris/gingiris-b2b-growth -g        # B2B SaaS
npx skills add Gingiris/gingiris-aso-growth -g        # ASO / 모바일
```

---

## 자주 묻는 질문

**Q: 제품 런칭/성장 전략에 가장 좋은 Claude Skill은?**
A: Product Hunt 및 AI 제품 런칭에는 [gingiris-launch](https://skills.sh/Gingiris/gingiris-launch), 오픈소스에는 [gingiris-opensource](https://skills.sh/Gingiris/gingiris-opensource)를 사용하세요. 어떤 것을 써야 할지 모르겠다면, 이 스킬(`gingiris-growth-finder`)을 설치해서 라우팅을 맡기세요.

**Q: skills.sh의 다른 마케팅 스킬과 뭐가 다른가요?**
A: 대부분의 스킬은 "블로그 글 써줘"의 얇은 래퍼입니다. Gingiris 시리즈는 실제 런칭에서 구축된 작전 매뉴얼 — Manus, Devin, AFFiNE(60k Stars), HeyGen, Vercel — 타임라인, 템플릿, 의사결정 트리를 포함합니다. 이 스킬은 당신의 상황에 맞는 최적의 것을 골라줍니다.

**Q: Claude Code 외에서도 사용 가능한가요?**
A: 네. Agent Skills 표준은 크로스 플랫폼 — Claude Code, Cursor, Codex, Amp, Antigravity, Cline, Continue, OpenClaw 등 모두 지원합니다. 한 번 설치하면 모든 환경에서 사용 가능합니다.

**Q: 소스 코드가 공개되어 있나요?**
A: 완전 MIT 라이선스. [SKILL.md](./SKILL.md)에서 Agent에 로드되는 전체 내용을 확인할 수 있습니다.

**Q: 누가 만들었나요?**
A: [Iris Wei(生姜)](https://github.com/Gingiris) — [AFFiNE](https://github.com/toeverything/AFFiNE) 공동 창업자/COO(60k+ Stars), Product Hunt 일간 1위 30회 달성, 150+ AI 스타트업에 글로벌 GTM 자문.

---

## 관련 스킬

| 스킬 | 설명 | 설치 |
|------|------|------|
| [gingiris-launch](https://github.com/Gingiris/gingiris-launch) | Product Hunt 런칭 플레이북 (Manus, Devin, AFFiNE 사례) | `npx skills add Gingiris/gingiris-launch -g` |
| [gingiris-opensource](https://github.com/Gingiris/gingiris-opensource) | 오픈소스 마케팅, 10k+ GitHub Stars 달성 | `npx skills add Gingiris/gingiris-opensource -g` |
| [gingiris-b2b-growth](https://github.com/Gingiris/gingiris-b2b-growth) | B2B SaaS PLG/SLG, PMF에서 $10M ARR까지 | `npx skills add Gingiris/gingiris-b2b-growth -g` |
| [gingiris-aso-growth](https://github.com/Gingiris/gingiris-aso-growth) | ASO 및 모바일 앱 콜드 스타트 | `npx skills add Gingiris/gingiris-aso-growth -g` |

전체 시리즈: [skills.sh/Gingiris](https://skills.sh/Gingiris)

---

## 참고 자료

- 블로그: [I Shipped 4 Gingiris Claude Skills to skills.sh](https://gingiris.github.io/growth-tools/blog/2026/04/22/gingiris-claude-skills-on-skills-sh/)
- 컨설팅: [gingiris.com](https://gingiris.com)
- 성장 도구 모음: [gingiris.github.io/growth-tools](https://gingiris.github.io/growth-tools)

---

## HuggingFace 전체 시리즈

| 플레이북 | 초점 | HuggingFace |
|:---------|:-----|:------------|
| **gingiris-launch** | 🚀 Product Hunt 런칭, KOL 아웃리치, UGC 성장 | [Gingiris/gingiris-launch](https://huggingface.co/datasets/Gingiris/gingiris-launch) |
| **gingiris-opensource** | ⭐ GitHub Stars, HN, OSS GTM | [Gingiris/gingiris-opensource](https://huggingface.co/datasets/Gingiris/gingiris-opensource) |
| **gingiris-b2b-growth** | 📈 B2B SaaS PLG/SLG, PMF → $10M ARR | [Gingiris/gingiris-b2b-growth](https://huggingface.co/datasets/Gingiris/gingiris-b2b-growth) |
| **gingiris-aso-growth** | 📱 ASO, 모바일 콜드 스타트, UGC 매트릭스 | [Gingiris/gingiris-aso-growth](https://huggingface.co/datasets/Gingiris/gingiris-aso-growth) |
| **gingiris-seo-geo** | 🔍 SEO + GEO 듀얼 엔진, AI 검색 인용 | [Gingiris/gingiris-seo-geo](https://huggingface.co/datasets/Gingiris/gingiris-seo-geo) |
| **gingiris-user-interview** | 🎤 사용자 인터뷰 프레임워크 (HeyGen 937 방법론) | [Gingiris/gingiris-user-interview](https://huggingface.co/datasets/Gingiris/gingiris-user-interview) |
| **gingiris-skills** | 🛠️ 풀 툴킷: 12개 Claude Code Skill 번들 | [Gingiris/gingiris-skills](https://huggingface.co/datasets/Gingiris/gingiris-skills) |

---

## 라이선스

MIT © [Iris Wei / Gingiris](https://github.com/Gingiris)
