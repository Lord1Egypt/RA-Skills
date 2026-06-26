## Description: <br>
ISBN图书查询。输入 ISBN-10 或 ISBN-13，查询书名、作者、译者、出版社、出版日期、页数、定价、装帧、丛书和封面等信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to look up publication details for ISBN-10 or ISBN-13 identifiers through Jike's book data API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the ISBN and Jike AppKey to the disclosed Jike book-data API. <br>
Mitigation: Store the AppKey in an environment variable and avoid passing it on the command line. <br>
Risk: The optional JIKE_API_BASE_URL override can redirect requests to a non-default endpoint. <br>
Mitigation: Leave JIKE_API_BASE_URL unset or set it only to a trusted compatible HTTPS endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-book-isbn-query) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Jike ISBN query endpoint](https://api.jikeapi.cn/v1/book/isbn/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text or JSON from a Python command-line script, usually summarized as Markdown by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ISBN input and a Jike AppKey supplied through JIKE_BOOK_ISBN_QUERY_KEY or JIKE_APPKEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
