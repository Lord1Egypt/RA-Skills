## Description: <br>
Creates a KakaoTalk channel AI agent with Vercel serverless deployment and an optional relay mode that connects to a local computer for memory and file-backed responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifeissea](https://clawhub.ai/user/lifeissea) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and KakaoTalk channel operators use this skill to deploy a KakaoTalk chatbot endpoint on Vercel. Relay-mode users can route KakaoTalk messages through Supabase to a local agent for memory-aware or local-context responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relay mode can expose KakaoTalk chat content and local memory through cloud services and callback delivery. <br>
Mitigation: Use Basic mode unless relay behavior is needed; for Relay mode, use a dedicated Supabase project with least-privilege credentials and keep secrets out of MEMORY.md. <br>
Risk: Unrestricted or unvalidated callback destinations can send generated responses to unintended endpoints. <br>
Mitigation: Require Kakao signature validation, restrict callback destinations, and review callback URL handling before public deployment. <br>
Risk: Local launchd and ngrok helpers can keep services running or expose the local server publicly after testing. <br>
Mitigation: Disable launchd and ngrok helpers when not actively in use and avoid public tunnels unless they are required. <br>


## Reference(s): <br>
- [ClawHub Kakaotalk Skill Page](https://clawhub.ai/lifeissea/kakaotalk) <br>
- [Kakao i Open Builder Skill Response Format](https://i.kakao.com/docs/skill-response-format) <br>
- [Kakao Business](https://business.kakao.com) <br>
- [Vercel Deployment Platform](https://vercel.com) <br>
- [Supabase](https://supabase.com) <br>
- [Local Kakao API Reference Summary](artifact/references/kakao-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and deployment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Kakao Open Builder setup guidance, Vercel deployment commands, Supabase relay configuration, and local runtime helper commands.] <br>

## Skill Version(s): <br>
1.2.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
