# Prompt Library

Store, organize, and retrieve reusable prompt templates. Stop rewriting the same prompts — build a personal library.

## Tools

### prompt_save
Save a prompt template to your library.

**Parameters:**
- `name` (string, required): Short name for the prompt (e.g. "blog-outline", "sales-email")
- `template` (string, required): The prompt template text. Use {{variable}} for placeholders.
- `category` (string, optional): Category tag (e.g. "writing", "coding", "research", "sales")
- `description` (string, optional): Brief description of what the prompt does
- `variables` (string[], optional): List of variable names used in the template

**Returns:** Confirmation with prompt ID.

### prompt_search
Search your prompt library by keyword or category.

**Parameters:**
- `query` (string, optional): Search term to match against name, description, or template content
- `category` (string, optional): Filter by category
- `limit` (number, optional): Max results, default 10

**Returns:** List of matching prompts with name, category, and preview.

### prompt_use
Retrieve a prompt template and fill in variables.

**Parameters:**
- `name` (string, required): Name of the saved prompt
- `variables` (object, optional): Key-value pairs to fill in {{variable}} placeholders

**Returns:** The filled prompt, ready to use.

### prompt_list_categories
List all categories in your library with prompt counts.

**Returns:** Category names and counts.

### prompt_delete
Remove a prompt from your library.

**Parameters:**
- `name` (string, required): Name of the prompt to delete

**Returns:** Confirmation.

### prompt_export
Export your entire prompt library as JSON.

**Returns:** Full library data.

## Storage

Prompts are stored in `memory/prompts/` as individual markdown files for easy version control and portability.

## Example Usage

```
Save: prompt_save name="cold-email" template="Hi {{name}}, I noticed {{observation}}. I built {{product}} that could help with {{pain_point}}. Would you be open to a quick look?" category="sales"

Search: prompt_search query="email" category="sales"

Use: prompt_use name="cold-email" variables={"name": "Alex", "observation": "your team ships weekly", "product": "a deployment tracker", "pain_point": "release coordination"}
```

## Why This Exists

Agents that build up prompt libraries become more efficient over time. Instead of crafting prompts from scratch each session, reuse what works. Compound your prompt engineering.

## Tags
utility, productivity, prompts, templates, writing
