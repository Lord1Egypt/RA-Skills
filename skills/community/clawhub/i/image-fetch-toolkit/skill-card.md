## Description: <br>
Image Fetch Toolkit helps agents search, fetch, and curate online images for papers, news, stock photography, products, scientific illustrations, social media, and academic figure composition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newtontech](https://clawhub.ai/user/newtontech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content creators use this skill to guide agents through online image search, API-based image retrieval, licensing checks, attribution, and academic figure assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Third-party image, news, academic, social, and search APIs may receive sensitive query terms. <br>
Mitigation: Avoid confidential or regulated search terms and use only providers approved for the user's environment. <br>
Risk: API keys and access tokens are needed for several providers. <br>
Mitigation: Configure only the keys required for the task, store them in environment variables or approved secret stores, and rotate any exposed credentials. <br>
Risk: Fetched images may carry license, attribution, platform terms, or reuse restrictions. <br>
Mitigation: Check image licenses, creator attribution requirements, and provider terms before using images in publications, products, or commercial work. <br>
Risk: Optional external tools and MCP servers may introduce additional operational or supply-chain risk. <br>
Mitigation: Review optional tools before installation and install only the integrations needed for the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/newtontech/image-fetch-toolkit) <br>
- [Unsplash API documentation](https://unsplash.com/developers) <br>
- [Pexels API documentation](https://www.pexels.com/api/) <br>
- [Pixabay API documentation](https://pixabay.com/api/docs/) <br>
- [Flickr API documentation](https://www.flickr.com/services/apps/) <br>
- [Google Custom Search documentation](https://developers.google.com/custom-search) <br>
- [Bing Image Search API](https://www.microsoft.com/en-us/bing/apis/bing-image-search-api) <br>
- [Semantic Scholar API](https://api.semanticscholar.org/graph/v1/paper/search) <br>
- [arXiv API](http://export.arxiv.org/api/query) <br>
- [PubMed Central Open Access API](https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi) <br>
- [Wikimedia Commons API](https://commons.wikimedia.org/w/api.php) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, API examples, configuration notes, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require user-supplied API keys and manual review of fetched image licenses, attribution, and provider terms.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
