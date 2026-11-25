# Materials: a small order service

[Chinese edition](https://github.com/gengshupeng/open-x-sys/blob/main/skills/open-x-sys.zh-CN/experience/playground/subjects/sample-codebase/ABOUT.md)

> **A ready subject for the Playground: a sample codebase.**
> This is a **constructed sample**, written for the Playground. It is small enough to read in a few minutes and runs with the Python standard library only (Python 3.10 or later): `python -m unittest` in this folder.
> It was built to be worth opening a system for. Its documentation and its code do not always agree, and its behavior under load is not what a first reading suggests. **This file does not say where.** Finding that is the run.

## Files

| File | What it is |
|---|---|
| `README.md` | The project's own documentation, as its authors wrote it |
| `orders.py` | The order queue and the workers |
| `inventory.py` | Stock reservation |
| `notify.py` | Customer notification |
| `test_orders.py` | The tests |

## How to use it as a subject

- Treat the code as the evidence. Every judgment should point to a file and a line, and anything that can be run should be run if the host allows.
- Good first prompts: "Open a system for this codebase." · "Follow one order through this service." · "What really limits how many orders per second this can handle?" · "What would make this fail on a busy day?"
- The understanding is "as of" this folder's current contents.
