## Description: <br>
Generates 1024x1024 Chinese GlucoDNA kidney-protection advertising images with product imagery using the Gemini API and bundled product information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangyisheng9-bot](https://clawhub.ai/user/jiangyisheng9-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams and agents supporting Chinese-language GlucoDNA campaigns use this skill to generate square product ad images with product photos, campaign copy, pricing, and contact details. <br>

### Deployment Geography for Use: <br>
Malaysia <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Gemini API key. <br>
Mitigation: Use a dedicated, limited API key through an environment variable and avoid storing broad credentials in shared files. <br>
Risk: Generated ads may reuse customer-derived health testimonials or make regulated health-product claims. <br>
Mitigation: Confirm testimonial consent, remove unnecessary personal details, and have health-product claims reviewed for advertising and compliance requirements before publication. <br>
Risk: The packaged product knowledge includes sales and order-handling guidance for a health product. <br>
Mitigation: Review generated copy before use and keep ordering, pricing, and contact details accurate for the intended market. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiangyisheng9-bot/glucodna-ad-generator) <br>
- [GlucoDNA product image](https://hk3.com.my/wp-content/uploads/2024/04/PRODUCT-SIZE-500PX-07.png) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image file with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Gemini API key; the default output path is ~/Desktop/GlucoDNA_广告图.png unless a path argument is supplied.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
