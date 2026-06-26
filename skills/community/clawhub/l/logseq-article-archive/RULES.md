# Logseq Data Architecture Maintenance Rules

## 1. Architecture Definition

### 1.1 Three-Layer Architecture
- **Raw Materials Layer**: Stored in the `logseq/pages/` directory. May be modified as necessary (e.g., adding titles, summaries, and cross-references) to avoid becoming orphan documents
- **Index Files Layer**: Stored in the `logseq/pages/index/` directory, managed by LLM
- **Rule Files Layer**: Stored in the skill's directory alongside SKILL.md

### 1.2 Index Structure
- **First-level Index**: `contents.md` - Main entry point for the master index, containing knowledge base index and system function index, linking to index pages for various domains (located in the `pages` directory)
- **Second-level Index**: `../pages/index/Knowledge Base Index.md` - Detailed knowledge base index containing detailed categories for various domains (located in the `index` directory, at the same level as `pages`), excluding system function index
- **Third-level Index**: `../pages/index/Investment Index.md`, `../index/Technology Index.md`, etc. - Contains specific content categories and links (located in the `index` directory, at the same level as `pages`)

### 1.3 Index File Types
- **Summary Pages**: Summarize the core content of raw materials
- **Entity Pages**: Detailed information about specific entities
- **Concept Pages**: Detailed information about abstract concepts
- **Comparison Pages**: Comparisons between different entities or concepts
- **Overview Pages**: General introductions to a field
- **Synthesis Pages**: Comprehensive analysis from multiple sources
- **Index Pages**: Indexes for categorization and navigation
- **Log Pages**: Records of processing steps and important findings

## 2. Naming Conventions

### 2.1 File Naming
- Use English titles that clearly describe page content
- Avoid special characters, use spaces to separate words
- For series pages, use consistent naming format

### 2.2 Page Links
- Use Logseq bidirectional link format: `[[Page Name]]`
- Links should accurately reflect the content of the target page
- Establish cross-references between related pages

## 3. Content Structure

### 3.1 Page Structure
- **Title**: Use `#` level heading as the page main title
- **Summary**: Provide a brief summary at the beginning of the page
- **Main Content**: Organize content using list formats such as `-` or `1.`
- **Cross-references**: Add bidirectional links at relevant content
- **Source Citations**: Indicate information sources, especially content from raw materials

### 3.2 Format Specifications
- Use Markdown format
- Use bold (**), italic (*), etc., appropriately
- For important information, use blockquotes (>)
- Maintain consistent indentation and formatting style

## 4. Workflow

### 4.1 Document Writing Workflow
1. **Material Analysis**: Read raw materials, extract core content and key concepts
2. **Summary Generation**: Create summary page, summarizing the main content of the material
3. **Entity Extraction**: Identify and create independent pages for related entities
4. **Concept Extraction**: Identify and create independent pages for related concepts
5. **Content Relevance Analysis**: Analyze the relevance of words and sentences in the document content to existing content
6. **Bidirectional Link Editing**: Edit relevant content using bidirectional links, linking to related pages
7. **Cross-references**: Create links between related pages
8. **Index Update**: Update relevant index pages
9. **Log Recording**: Add processing record to the log page

### 4.2 Orphan Document Processing Workflow
1. **Traversal Scanning**: Traverse all documents in the pages directory
2. **Structure Check**: Check if each document contains title, summary, and cross-references
3. **Reference Analysis**: Analyze the reference status of each document, identify orphan documents
4. **External Link Creation**: Create external links for all documents to ensure linking with other related documents
5. **Cross-references**: Establish bidirectional links between related pages
6. **Index Update**: Update relevant index pages to ensure all documents are indexed

### 4.3 Document Standardization Workflow
1. **Title Addition**: Add main title (# level heading) to all documents
2. **Summary Generation**: Add brief summaries to all documents, summarizing the main content
3. **Cross-reference Addition**: Add cross-references to all documents, linking to related pages
4. **Format Standardization**: Ensure consistent document format, using Markdown format
5. **Index Inclusion**: Ensure all documents are included in relevant index pages

### 4.4 Query Workflow
1. **Question Analysis**: Understand the intent and scope of the user's query
2. **Material Search**: Search relevant index pages
3. **Information Synthesis**: Synthesize information from multiple pages
4. **Answer Generation**: Generate appropriate forms of answers based on query requirements
5. **Source Citations**: Indicate information sources
6. **Page Archiving**: Archive valuable answers as new pages

### 4.5 Health Check Workflow
1. **Comprehensive Scanning**: Scan all index pages
2. **Issue Identification**: Identify contradictions between pages, outdated statements, etc.
3. **Orphan Page Detection**: Find orphan pages with no incoming links
4. **Concept Page Detection**: Identify important concepts mentioned but lacking independent pages
5. **Cross-reference Check**: Check for missing cross-references
6. **Data Gap Detection**: Discover data gaps that can be filled by web search
7. **Report Generation**: Generate health check report and improvement suggestions

## 5. Quality Standards

### 5.1 Content Quality
- **Accuracy**: Ensure accurate information from reliable sources
- **Completeness**: Cover the main content and key concepts of materials
- **Consistency**: Maintain consistent information between pages
- **Clarity**: Clear expression with reasonable structure

### 5.2 Link Quality
- **Relevance**: Links should be relevant to page content
- **Accuracy**: Link targets should accurately reflect link text
- **Completeness**: Important concepts and entities should have corresponding links
- **Content Relevance**: Words and sentences in document content that are related to existing content should be edited using bidirectional links
- **Link Density**: Use bidirectional links appropriately, avoiding excessive linking that affects reading experience

### 5.3 Structure Quality
- **Clear Hierarchy**: Page structure should be well-organized for easy reading
- **Consistent Format**: Maintain consistent format and style
- **Easy Navigation**: Facilitate navigation through indexes and cross-references

## 6. Special Handling

### 6.1 Multi-source Materials
- For the same topic from multiple sources, create synthesis pages
- Indicate contributions and differences from each source
- Maintain consistency and completeness of information

### 6.2 Complex Concepts
- For complex concepts, create dedicated concept pages
- Use diagrams, examples, etc., to aid understanding
- Provide cross-references to related concepts

### 6.3 Controversial Content
- For controversial content, objectively present different viewpoints
- Indicate sources and basis for each viewpoint
- Avoid bias and subjective judgment

## 7. Maintenance Cycle

### 7.1 Daily Maintenance
- Update related pages after processing new materials
- Regularly check consistency between pages
- Fix issues promptly when discovered

### 7.2 Regular Health Checks
- Conduct a comprehensive health check monthly
- Perform in-depth analysis and optimization quarterly
- Conduct comprehensive architecture evaluation and adjustment annually

## 8. Collaboration Standards

### 8.1 User Interaction
- Maintain active interaction with users to understand their needs and preferences
- Accept user feedback and suggestions
- Adjust work focus according to user guidance

### 8.2 Work Records
- Record processing steps and important decisions
- Maintain transparent workflow
- Regularly report work progress to users

## 9. Continuous Improvement

### 9.1 Rule Optimization
- Regularly evaluate and optimize rules
- Adjust workflows based on actual usage
- Learn and apply new knowledge management methods

### 9.2 Technological Innovation
- Explore new visualization methods
- Try new organization and classification methods
- Utilize new technologies to improve efficiency and quality

## 10. Emergency Handling

### 10.1 Error Handling
- Detect and fix errors promptly
- Record error causes and resolution methods
- Prevent recurrence of similar errors

### 10.2 Data Recovery
- Regularly backup index files
- Establish data recovery mechanisms
- Ensure data can be recovered in case of accidents

### 10.3 Performance Optimization
- Monitor system performance
- Identify and resolve performance bottlenecks
- Ensure system response speed and stability

## Conclusion

This rule file defines the core principles and workflows for Logseq data architecture maintenance, aiming to help LLM become a disciplined index maintainer. As usage deepens, these rules will evolve together with the user to adapt to the needs and characteristics of specific domains. By following these rules, LLM will be able to build and maintain a high-quality, sustainable Logseq data architecture.
