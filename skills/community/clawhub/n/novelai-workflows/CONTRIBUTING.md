# Contributing

Contributions are welcome, especially improvements to NovelAI/OpenClaw compatibility, Chinese and English usage documentation, prompt workflows, and safe metadata handling.

## Before opening a pull request

- Read `SKILL.md` and preserve its credential-safety rules.
- Do not commit `.env`, tokens, live API output, account reports, generated images, or local archives.
- Keep the Skill frontmatter name `openclaw-novelai` stable.
- Update the documentation when a tool signature, model ID, endpoint, or upstream version changes.
- Add or update offline tests for payload and workflow behavior.

Run the offline checks:

```powershell
python -m unittest discover -s tests -v
python -m py_compile scripts\project_state.py scripts\live_api_test.py tests\test_project_state.py tests\test_skill_contract.py tests\test_live_api_test.py
```

Live API checks are opt-in, can consume Anlas, and must use only a test account or a credential supplied by the contributor outside the repository. Never include the credential or raw response body in a pull request.
