# Unusual Movements Invoke Contract

This file is a reference note for the JS skill. It is not executable code.

The original backend invoke flow does these things before calling the model:

1. Load a long K-line window.
2. Build support and resistance context.
3. Build market technical status text.
4. Collect recent trading days and recent prices.
5. Load historical reports.
6. Render the final prompt with system prompt, extra requirements, and user template.

In this skill repo, only the prompt assets remain local. Data fetching and preprocessing stay outside this file.
