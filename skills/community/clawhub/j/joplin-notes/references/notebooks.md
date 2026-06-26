# Joplin Notebook IDs (Reference)

This file serves to document the IDs of your Joplin notebooks.

## How to Find a Notebook ID?
You can use the `list_notes.py` script to list all available notebooks and their IDs:
`python3 scripts/list_notes.py`

## Known IDs (Examples)
| Name | Notebook ID (parent_id) | Description |
| :--- | :--- | :--- |
| **Example Notebook** | `your_notebook_id_here` | A container for notes. |

## Important Notes
- **type_: 2** indicates in the Joplin data structure that this file represents a notebook.
- Notes (Type 1) in these notebooks have the corresponding Notebook ID as `parent_id`.
- IDs are permanent unless the notebook is deleted.
