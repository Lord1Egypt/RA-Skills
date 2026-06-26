# JSON Key Sorter

This utility standardizes JSON data by sorting all keys within JSON objects alphabetically. This makes JSON files easier to compare (diff), ensures consistent API responses, and improves readability, saving developers time and reducing merge conflicts.

## Usage

1.  **Sort a JSON file and print to console:**
    ```bash
    python tool.py my_data.json
    ```
2.  **Sort a JSON file and save to a new file:**
    ```bash
    python tool.py my_data.json -o sorted_data.json
    ```
3.  **Pipe JSON from another command
