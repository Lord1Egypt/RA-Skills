# QA Cases

Use these cases to test whether answers stay provider-specific and conservative. Expected checkpoints focus on evidence behavior, not hard-coded support conclusions.

1. Does Claude on Bedrock support a newly announced Anthropic feature?
   - Checks AWS Bedrock official docs for Bedrock support.
   - Uses Anthropic docs only as comparison context.
   - Marks unknown if AWS docs do not confirm.

2. Is Claude on Vertex AI feature-parity with Anthropic's API?
   - Checks Google Vertex AI Claude partner docs.
   - Avoids claiming parity from Anthropic docs alone.
   - Calls out provider-specific API and region differences.

3. Which Claude model ID should I use in Bedrock?
   - Cites AWS Bedrock supported models or model parameter docs.
   - Distinguishes AWS model IDs from Anthropic model names.
   - Mentions live check for region/model availability.

4. Can I use Anthropic Messages API examples unchanged on Bedrock?
   - Checks AWS Bedrock Anthropic parameter docs.
   - Identifies Bedrock request wrapping/auth differences if documented.
   - Does not paste large official examples.

5. Can I use Claude computer-use/tool-use on Vertex AI?
   - Checks Google Cloud Vertex Claude docs for exact capability.
   - If only Anthropic docs mention it, returns unknown for Vertex.
   - Notes model/version/API surface requirements.

6. Does Azure OpenAI support the latest OpenAI Responses API feature?
   - Checks Microsoft Azure OpenAI reference and API version docs.
   - Uses OpenAI docs only to explain first-party behavior.
   - Does not assume Azure parity.

7. Is an OpenAI model announced today available in Azure?
   - Checks Microsoft model availability docs and region/version notes.
   - Distinguishes OpenAI launch availability from Azure deployment availability.
   - Marks unknown if Microsoft docs are not updated.

8. Can Azure OpenAI use the same model name as OpenAI API?
   - Checks Azure deployment/model docs.
   - Explains deployment names and Azure model/version concepts.
   - Avoids claiming first-party naming compatibility unless Microsoft confirms.

9. Is a Foundry model catalog entry callable through Azure OpenAI API?
   - Checks Azure AI Foundry docs and Azure OpenAI docs separately.
   - Distinguishes catalog availability from service/API availability.
   - Asks for target endpoint if ambiguous.

10. Does Azure support a specific OpenAI tool/function-calling parameter?
    - Checks Azure OpenAI API reference for the requested API version.
    - Compares with OpenAI API reference only as context.
    - Marks provider-specific or unknown if parameter behavior differs or is absent.

11. Does Vertex AI Gemini support a feature shown in ai.google.dev examples?
    - Checks Google Cloud Vertex AI Gemini docs/reference.
    - Treats Gemini API docs as first-party developer API only.
    - Marks unknown for Vertex if Google Cloud docs do not confirm.

12. Can Gemini API code be copied directly to Vertex AI?
    - Checks both Gemini API and Vertex AI docs.
    - Calls out endpoint/auth/SDK/model naming differences.
    - Avoids unsupported portability claims.

13. Which Gemini model versions are available in Vertex AI in a given region?
    - Checks Vertex AI model docs and region availability docs.
    - Does not use ai.google.dev alone for region claims.
    - Requires live check if region is production-critical.

14. Does Gemini API support enterprise IAM or VPC controls?
    - Checks Gemini API docs for direct API behavior.
    - Checks Vertex AI docs if user actually needs Google Cloud enterprise controls.
    - Recommends clarifying target service when ambiguous.

15. Are context windows identical across OpenAI, Azure, Bedrock, and Vertex-hosted variants?
    - Checks exact provider/model/version docs.
    - Avoids deriving limits from shared model family names.
    - Records partial/provider-specific when limits vary.

16. Which provider should we cite when support docs conflict?
    - Prefers hosting provider docs for hosted API claims.
    - Mentions conflict and date/last-reviewed context.
    - Recommends live verification for production decisions.

17. Can we promise feature support to a customer based on vendor blog posts?
    - Requires official docs, model cards, or API reference.
    - Treats blog/marketing pages as non-authoritative unless backed by docs.
    - Uses conservative language for unverified claims.

18. What should the answer say when official docs cannot be fetched?
    - Keeps registry URL and access notes.
    - States access limitation clearly.
    - Uses `unknown_needs_live_check` rather than guessing.
