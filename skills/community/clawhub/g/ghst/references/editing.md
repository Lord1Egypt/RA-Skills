# Editing Posts and Pages

When a user asks you to edit the content of a post or a page, you must understand your limitations. Ghost stores rich markup in distinct, structured Lexical JSON nodes. Modifying the rich styling or adding complex new elements directly in the JSON is extremely error-prone. 

Because of this, your editing capabilities are restricted to:
1. **Minor rewording** in the text.
2. **Changing URLs** of links.

You should read the content, find the specific text node or link node requested by the user, edit the text string or URL while leaving the rest of the Lexical node styling alone, and update the post or page.

The `ghst` CLI supports this "Read-Edit-Write" workflow for Lexical content. Follow these exact steps:

1. **Extract the Lexical content to a file**
   Use the `--formats lexical` flag to include the content and the `--json` flag to request raw data. You will use `jq` to isolate the string and save it to a JSON file.

   For a post:
   ```bash
   ghst post get <POST_ID> --formats lexical --json | jq -r '.posts[0].lexical' > content.json
   ```

   For a page:
   ```bash
   ghst page get <PAGE_ID> --formats lexical --json | jq -r '.pages[0].lexical' > content.json
   ```
   *Note: Ghost stores its Lexical content as a stringified JSON object. Using `jq -r` creates a file that contains the workable JSON structure of the Lexical tree, rather than a quoted string.*

2. **Edit the file**
   Read `content.json` to find the target text or URL and modify it within its corresponding JSON node. **Do not alter the structure, types, or styling**.

3. **Update the post/page with the edited file**
   Use the `--lexical-file` option on the update command. The CLI automatically reads the file, re-stringifies it, and updates the post or page on the server.

   For a post:
   ```bash
   ghst post update <POST_ID> --lexical-file content.json
   ```

   For a page:
   ```bash
   ghst page update <PAGE_ID> --lexical-file content.json
   ```
