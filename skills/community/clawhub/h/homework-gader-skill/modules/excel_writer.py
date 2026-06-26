import pandas as pd
import os

def save_to_excel(data, assignment_id):
    os.makedirs("data/results", exist_ok=True)

    path = f"data/results/assignment_{assignment_id}.xlsx"

    df = pd.DataFrame(data)
    df.to_excel(path, index=False)

    return path