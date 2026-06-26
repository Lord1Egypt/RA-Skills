---
name: Gradio
description: Build and deploy ML demo interfaces with proper state management, queuing, and production patterns.
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

# Gradio Patterns

## Interface vs Blocks
- `gr.Interface` is for single-function demos — use `gr.Blocks` for anything with multiple steps, conditional UI, or custom layout
- Blocks gives you `.click()`, `.change()`, `.submit()` event handlers — Interface only has one function
- Mixing Interface inside Blocks works but creates confusing state — pick one pattern per app

## State Management
- `gr.State()` creates per-session state — it resets when the user refreshes the page
- State values must be JSON-serializable or Gradio silently drops them — no custom classes without serialization
- Pass State as both input AND output to persist changes: `fn(state) -> state` — forgetting the output loses updates
- Global variables shared across users cause race conditions — always use `gr.State()` for user-specific data

## Queuing and Concurrency
- Without `.queue()`, long-running functions block all other users — always call `demo.queue()` before `.launch()`
- `concurrency_limit=1` on a function serializes calls — use for GPU-bound inference that can't parallelize
- `max_size` in queue limits waiting users — without it, memory grows unbounded under load
- Generator functions with `yield` enable streaming — but they hold a queue slot until complete

## File Handling
- Uploaded files are temp paths that get deleted after the request — copy them if you need persistence
- `gr.File(type="binary")` returns bytes, `type="filepath"` returns a string path — mismatching causes silent failures
- Return `gr.File(value="path/to/file")` for downloads, not raw bytes — the component handles content-disposition headers
- File uploads have a default 200MB limit — set `max_file_size` in `launch()` to change it

## Component Traps
- `gr.Dropdown(value=None)` with `allow_custom_value=False` crashes if the user submits nothing — set a default or make it optional
- `gr.Image(type="pil")` returns a PIL Image, `type="numpy"` returns an array, `type="filepath"` returns a path — inconsistent inputs break functions
- `gr.Chatbot` expects list of tuples `[(user, bot), ...]` — returning just strings doesn't render
- `visible=False` components still run their functions — use `gr.update(interactive=False)` to disable without hiding

## Authentication
- `auth=("user", "pass")` is plaintext in code — use `auth=auth_function` for production with proper credential checking
- Auth applies to the whole app — there's no per-route or per-component auth without custom middleware
- `share=True` with auth still exposes auth to Gradio's servers — use your own tunnel for sensitive apps

## Deployment
- `share=True` creates a 72-hour public URL through Gradio's servers — not for production, just demos
- Environment variables in local dev don't exist in Hugging Face Spaces — use Spaces secrets or the Settings UI
- `server_name="0.0.0.0"` to accept external connections — default `127.0.0.1` only allows localhost
- Behind a reverse proxy, set `root_path="/subpath"` or assets and API routes break

## Events and Updates
- Return `gr.update(value=x, visible=True)` to modify component properties — returning just the value only changes value
- Chain events with `.then()` for sequential operations — parallel `.click()` handlers race
- `every=5` on a function polls every 5 seconds — but it holds connections open, scale carefully
- `trigger_mode="once"` prevents double-clicks from firing twice — default allows rapid duplicate submissions

## Performance
- `cache_examples=True` pre-computes example outputs at startup — speeds up demos but increases load time
- Large model loading in the function runs per-request — load in global scope or use `gr.State` with initialization
- `batch=True` with `max_batch_size=N` groups concurrent requests — essential for GPU throughput
