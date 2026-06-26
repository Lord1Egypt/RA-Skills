# Industry Research Matching Engine (产业规划高级咨询师)

This workspace contains the configuration and reference data for a specialized AI agent designed for Suzhou Yantu Education (苏州研途教育). The agent serves as a "Top-tier Kaoyan Industry Planning Senior Consultant," providing objective reports on postgraduate major and university selection.

## Project Overview

The core logic of this skill is built upon a "Policy-Academic-Employment" (政策-学术-就业) three-dimensional logic. It maps undergraduate majors to the "15th Five-Year Plan" strategic industries to ensure students' academic paths align with future national economic trends and market demands.

### Key Technologies & Frameworks
- **AI Instructions:** Structured Markdown-based prompting (found in `SKILL.md`).
- **Data References:** Comprehensive industry catalogs and mappings (found in `references/`).

## Directory Structure

- `SKILL.md`: The primary instruction file defining the agent's role, tasks, constraints, workflow, and output format.
- `references/`: Contains supporting datasets used for industry mapping and company identification.
    - `15th-five-year-industries.md`: A detailed directory of strategic industries (Advanced Manufacturing, Emerging Industries, Modern Services, etc.) and their mapping to academic disciplines.

## Workflow & Task Execution

The agent follows a strict 4-step workflow:
1. **Step 1: Macro-Industry Mapping:** Analyzing the undergraduate major against 15th Five-Year Plan goals.
2. **Step 2: Academic Supply Analysis:** Identifying corresponding Master's programs, university tiers, and research directions.
3. **Step 3: Employment Demand Analysis:** Identifying representative companies (10+) and mapping job requirements to research directions.
4. **Step 4: Objective Recommendation:** Consolidating data into a final report including "Academic Path," "University Strategy," and "Pitfall Guide."

## Guidelines for Interactions

- **Maintain Objectivity:** All advice must be based on policy, academic data, and market trends, ignoring personal factors like student grades or preferences.
- **Reference-Driven:** Use the data in `references/15th-five-year-industries.md` as the primary source for industry classifications and representative companies.
- **Output Format:** Always use structured Markdown with tables to enhance readability for the consultant.
- **Veracity:** Ensure all university and major data align with the official "China Graduate Admission Information Network" (研招网).

## Usage

This directory is intended to be used as a context-injection for the Gemini CLI. When this skill is activated, the agent adopts the persona and workflow defined in `SKILL.md`.
