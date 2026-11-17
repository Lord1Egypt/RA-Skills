# Meal Planner and Grocery List input contract

plan: meals [{date,slot breakfast|lunch|dinner,dish,servings,ingredients:[{name,quantity,unit}]}], optional exclude [ingredient names], pantry [{name,quantity,unit}], budget {amount,currency}. Quantities cover the meal’s total servings. g/kg and ml/l are normalized; different unconvertible units remain separate. show: id. Plan writes require requestId.

## Added in 1.1.0

New: preferences {exclude:[],pantry:[{name,quantity,unit}]} replaces saved preferences; show-preferences reads them. scale {id,servings,pantry:[]} creates a separate plan. export {id} writes menu and groceries. A pantry is a snapshot, not automatically consumed stock. Writes/exports require requestId.

## Output files

meal-plan.md / groceries.csv

Exports create a new unique directory and return files [{path,bytes,sha256}]. Repeating the same requestId returns the same files; altered or missing saved exports raise an error. CSV output quotes fields and neutralizes spreadsheet formula prefixes. Keep other operations' active lock files in place. All files and records are scoped to the supplied active workspace.
