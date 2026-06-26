export async function aiReview(code: string, llm: any) {

    const prompt = `
Analyze the following code for malicious behavior.

Check for:
- data exfiltration
- shell execution
- credential leak
- system modification

Code:
${code}

Return JSON:
risk_level
reason
`

    const result = await llm.generate(prompt)

    return result

}