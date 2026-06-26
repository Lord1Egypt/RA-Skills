---
name: sp-analysis
description: You are an expert in Oracle SQL. Search the SP (Stored Procedure) name from the chatbox in the SQL package and analyze. LLM base model temperature should be 0. Analyze the data flow of Oracle stored procedures (SPs) within a package, showing complete dependency chains from Upstream SP to downstream SP. And then show the target SP details. Ensure no steps are skipped, and all relevant SPs are included.
argument-hint: Input [SP Name] and attach [Package File]
version: 1.0
---

# Skill Instructions

## Investigation Steps  
1. Locate the target stored procedure (SP) within the package attached.

1.1. **Line-number accuracy first (mandatory):**
    - Always derive line numbers from the **actual workspace file content**.
    - Do **not** estimate or infer line numbers from summarized/truncated attachments.
    - Before writing output, re-open the relevant line ranges and verify each referenced start/end line exactly matches the cited statement.
    - For any `Invoking:` line, the referenced range must include the **exact call statement line** (single-line range is preferred for a single-line call).
    - If a call statement is on line `N`, output `[...:N](...#LN)` (or `[...:N-N](...#LN-LN)`), never a different line.
    - If exact line verification is not possible, do not guess; re-scan until exact lines are confirmed.

2. Identify all SPs that directly CALL the target SP.
   - Treat these as UPSTREAM SPs.
   - For each upstream SP, extract:
     - SP name
     - Invoking command
    - Procedure Body range in package body
    - Tables READ
    - Include a clickable reference such as `[JTA_Packages.sql:255-263](Demo_GC_Usage/03Development_Zone/Oracle_Package/JTA_Packages.sql#L255-L263)` so VS Code can jump directly to the lines where the call occurs (use workspace-relative paths).
    - The `255-263` range must be the **true** line range in the current file version.

3. Analyze the target SP body for Mechanism Analysis.
    - Break down the SP body into logical sections (e.g., Preparation, Data Loading, Transformations, Output).
    - For each section, summarize the key operations and data flow.
    - Every bullet ends with a clickable reference such as `[JTA_Packages.sql:255-263](Demo_GC_Usage/03Development_Zone/Oracle_Package/JTA_Packages.sql#L255-L263)` that points to the relevant lines in the package (workspace-relative path).


4. Within the target SP body, identify any SPs that the target SP CALLS.
    - Treat these as DOWNSTREAM SPs.
    - Extract for each downstream SP:
      - SP name
      - Call Line
      - Procedure Body location/range
      - Tables READ
    - Add clickable references like `[DOWNSTREAM(v1,v2)](Demo_GC_Usage/03Development_Zone/Oracle_Package/JTA_Packages.sql#L255-L263)` for call lines and body locations (workspace-relative path), ensuring the call line is in the [] and matches the actual call statement line in the package body.
    - The reference range must map to the exact call statement in the package body.

5. If Upstream SP or Downstream SP are null, double-check to avoid mistakes and use --None-- to indicate no Upstream SP or Downstream SP.
    - When value is `--None--`, do **not** append line numbers or markdown links to that `--None--` entry.
    - Do **not** add empty braces/objects such as `{}` for missing Upstream/Downstream items.
    - Examples:
    ```
    #### Upstream Procedures
    - None

    #### Downstream Procedures
    - None
    ```

6. Assemble the results using markdown headings exactly in this style (match example header format): `# #1 Dependency Analysis: *PROCEDURE_NAME()* in *PACKAGE_NAME*`, `#### Upstream Procedures`, `#### Downstream Procedures`, `# #2 Mechanism Analysis for *PROCEDURE_NAME()*`.
    - Use list/bullet formatting for procedures and details (no tree connectors).
    - Use `None` exactly for missing items in this section format.

7. Append the Mechanism Analysis and Body Script. Output strictly follows the defined "Output Structure". The output example is provided in ./examples/examples_output.md. Use bold and italics for SP names.

8. **Final validation pass (mandatory):**
    - Validate every markdown link target and every displayed line range (`file.sql:X-Y`) against the file.
    - Ensure displayed range and URL fragment are identical (e.g., display `255-263` and link `#L255-L263`).
    - Validate each `Invoking:` link against the exact call line in package body (e.g., `get_hours(...)` at line `353` must link to `#L353`).
    - Ensure no reference points to package spec lines when the claim is about package body logic.



## Output Structure

- When analyzing a specific stored procedure, present the relationship using this integrated hierarchy format shown below. Ensure the output strictly adheres to this structure.

    # #1 Dependency Analysis: *PROCEDURE_NAME()* in *PACKAGE_NAME*

    #### Upstream Procedures
    1. **`PROCEDURE_A`**
        - **Call Line**: `jta.PROCEDURE_NAME(v_d_time);` [JTA_Packages.sql:255](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L255)
        - **Procedure Body**: [JTA_Packages.sql:240-310](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L240-L310)
        - **Reads**: `TABLE_1`, `TABLE_2`
    2. **`PROCEDURE_B`**
        - **Call Line**: `jta.PROCEDURE_NAME(v_ntc_time);` [JTA_Packages.sql:263](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L263)
        - **Procedure Body**: [JTA_Packages.sql:500-560](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L500-L560)
        - **Reads**: `INTERMEDIATE_TABLE_1`, `TABLE_3`

    #### Downstream Procedures
    1. **`PROCEDURE_C()`**
        - **Call Line**: [PROCEDURE_C(v2)](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L312)
        - **Procedure Body**: [JTA_Packages.sql:301-340](../02Development_Zone/Oracle_Package/JTA_Packages.sql#L301-L340)
        - **Reads**: `work_hours`
    ----
    # #2 Mechanism Analysis for *PROCEDURE_NAME()*
    ## 1.Preparation
    - Input Parameters: ...
    - Output Parameters:...
     ## 2.Load Data
    - Select a single row from ....
    - Initialize the Variables:....
    ## 3.Transform and Logic Condition 
    - 1)....
    - 2)....
    - 3)....
    ## 4.Final Output
    Returns fd to caller; no table writes occur, exceptions are logged through jta_error.gd.
    ----
    # #3 Body Script of *PROCEDURE_NAME()*
    ```
    Create Procedure

    ```



- Body Script is the DDL script of the target SP body.
- In the headers and Internal Analysis contens, the SP name and the package name should be italics. Use markdown code style for the variables, parameters,functions,etc.


## Best practices
- ✓ Search for **all callers** of the target SP (not just one)
- ✓ Include **all procedures called within** the target SP
- ✓ Check for table reads in cursors, subqueries, and CTEs
- ✓ Include system sources (e.g., `SYSDATE`, `DUAL`)
- ✓ Search across multiple packages for public procedures
- ✓ Ensure no upstream or downstream SPs are omitted
- ✓ Avoid including any additional descriptions or commentary in the output



