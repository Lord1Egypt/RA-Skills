---
name: openplag
version: 1.0.0
description: Check an academic paper, thesis or essay for originality with OpenPlag Labs (free, no account). Use when the user asks to check a document for plagiarism, overlap, citation problems or originality, in any of eight languages (English, Hebrew, Arabic, Russian, French, Spanish, German, Chinese).
metadata:
  openclaw:
    homepage: https://openplaglabs.com
    requires:
      bins:
        - curl
---

# OpenPlag Labs: originality check for one document

OpenPlag Labs compares a document with a local index of more than 180 million open-access records (OpenAlex) and the open web. It returns a summary (verbatim overlap, which shared passages are cited, the top sources, an experimental writing indicator) and a link to the full report, valid for 24 hours. No account, no API key.

Full service description for agents: https://app.openplaglabs.com/llms.txt

## Rules (follow all of them)

1. **Ask the user first.** Before sending anything, tell the user that the document will be sent to OpenPlag Labs, an external service, that it is deleted when the check ends, and that the report is kept for 24 hours. Send only after they agree, with `"user_confirmed": true`.
2. **One document per user request.** Never send batches. Never split a long document into parts to get around the length limit.
3. **Do not poll fast.** A check takes 10 to 20 minutes. Ask for the result no more often than `poll_after_seconds` from the last answer.
4. **When a call is refused, obey it.** If `retry` is false, do not retry. If there is `retry_after_seconds`, wait at least that long or stop. Always pass `tell_user` on to the user.
5. **Always pass on the disclaimer** that comes with the result: a similarity report is not a finding of plagiarism, and the writing indicator is an experimental probability, not evidence.

Limits: documents up to 10,000 words; formats PDF, DOCX, DOC, ODT, RTF, TXT; one check at a time per network address; waiting times grow between checks (5, 15, 45, 135 minutes); at most 5 a day. People who need more can open a free account at https://openplaglabs.com/?src=agent

## Start a check

Send exactly one of `text`, `url` (a public link to a PDF, DOCX or TXT file), or `content_base64` together with `filename`.

Plain text:

```bash
curl -s -X POST https://app.openplaglabs.com/agent/v1/checks \
  -H "Content-Type: application/json" -H "X-Agent-Name: openclaw" \
  -d '{"user_confirmed": true, "text": "THE DOCUMENT TEXT"}'
```

A file on disk (build the JSON with a tool that escapes it safely, e.g. jq or python):

```bash
python3 -c 'import base64,json,sys; print(json.dumps({"user_confirmed": True, "filename": sys.argv[1].rsplit("/",1)[-1], "content_base64": base64.b64encode(open(sys.argv[1],"rb").read()).decode()}))' "/path/to/paper.pdf" \
  | curl -s -X POST https://app.openplaglabs.com/agent/v1/checks -H "Content-Type: application/json" -H "X-Agent-Name: openclaw" -d @-
```

The answer contains a `token`, `estimated_seconds_left` and `poll_after_seconds`. Tell the user the check has started and roughly how long it will take.

## Get the result

```bash
curl -s https://app.openplaglabs.com/agent/v1/checks/TOKEN
```

- `status` is `queued` or `running`: wait `poll_after_seconds`, then ask again.
- `status` is `done`: give the user the `summary`, the `disclaimer`, the `report_url` (valid 24 hours) and `tell_user`.
- `status` is `failed` or `ok` is false: tell the user the `message` and `tell_user`. Do not retry the same file.

## Reading the summary for the user

- `verbatim_overlap_percent` is the share of words that also appear, in the same order, in a source. Quoted passages and the reference list are not counted.
- A high number is not necessarily a problem (standard methods text, long legal quotations, an earlier version of the same paper), and a low number can still hide one uncited paragraph. Point the user to the report and to the passages marked "not cited".
- Paraphrase and translation candidates are never counted in the score; they are leads for a person to check.

## Also available as an MCP server

If your setup prefers MCP: `https://app.openplaglabs.com/mcp` (Streamable HTTP), tools `check_document` and `get_check`, same rules.
