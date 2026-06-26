# opendart-cli

비공식 DART OpenAPI Python CLI. 한국 기업의 공시·재무·지분 정보를 터미널에서 JSON으로 가져온다.

- 공시 검색, 기업 개황, 재무제표, 대주주/임원 지분
- 고유번호 자동 다운로드·캐시
- 한국어 오류 메시지, 에이전트 친화 JSON 출력

전체 사용법은 [SKILL.md](SKILL.md) 참고.

## 설치

```bash
pipx install opendart-cli
```

## API 키

https://opendart.fss.or.kr 에서 무료 발급 후:

```bash
export OPENDART_API_KEY="your_40_char_key"
```

## 예시

```bash
opendart corp-code --refresh
opendart find-corp "카카오"
opendart list --corp-code 00258801 --bgn 20260101 --end 20260420
opendart finance --corp-code 00258801 --bsns-year 2025 --reprt-code 11011
```

## 개발

```bash
git clone https://github.com/ChloePark85/opendart-cli
cd opendart-cli
pipx install -e .
pytest
```

## License

MIT
