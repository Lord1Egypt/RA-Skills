# Feedback Report Schema

## 1. Schema Overview

This document defines the JSON Schema for **structured feedback reports** generated after each test execution round during the post-development verification fix loop.

The feedback report serves as the communication contract between test execution and the AI Agent's fix cycle. Every time tests are run--whether in the automated fix loop (Phase 3) or the final validation gate (Phase 4)--a report conforming to this schema is produced. The Agent parses this report programmatically to determine:

- **What broke** -- grouped by root cause, ordered by impact
- **What to fix next** -- via `failures_grouped` clusters and `next_action`
- **Whether to keep fixing** -- via `gate_result` and iteration efficiency metrics
- **How quality is trending** -- via `fix_history` and round-over-round metric comparisons
- **When to stop** -- via convergence guards and anti-pattern detection

The schema is designed to be both machine-parseable (for Agent decision-making) and human-readable (for developer review of the final quality report).

---

## 2. JSON Schema Definition

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Post-Development Verification Feedback Report",
  "description": "Structured feedback report generated after each test execution round in the fix loop.",
  "type": "object",
  "required": [
    "round",
    "project_context",
    "metrics",
    "gate_result",
    "failures_grouped",
    "fix_history",
    "hidden_tests",
    "next_action",
    "anti_patterns_detected"
  ],
  "properties": {
    "round": {
      "type": "integer",
      "minimum": 1,
      "description": "Current fix loop iteration (1-based). Round 1 is the first execution after initial test generation."
    },
    "project_context": {
      "type": "object",
      "required": ["language", "framework", "test_runner", "realism_level"],
      "properties": {
        "language": {
          "type": "string",
          "description": "Primary programming language of the project (e.g., 'typescript', 'python', 'java')."
        },
        "framework": {
          "type": "string",
          "description": "Detected application framework (e.g., 'express', 'fastapi', 'spring-boot')."
        },
        "test_runner": {
          "type": "string",
          "description": "Detected test runner (e.g., 'jest', 'vitest', 'pytest', 'junit')."
        },
        "realism_level": {
          "type": "string",
          "enum": ["L0", "L1", "L2", "L3"],
          "description": "Test realism level. L0 = all dependencies mocked, L1 = core service real with databases mocked, L2 = internal services real with only uncontrollable external deps mocked, L3 = all services real using sandbox/test accounts."
        }
      }
    },
    "metrics": {
      "type": "object",
      "required": ["design_quality", "execution_quality", "delivery_quality", "iteration_efficiency"],
      "properties": {
        "design_quality": {
          "type": "object",
          "description": "Metrics measuring how well the test suite was designed to cover the requirements.",
          "required": [
            "scenario_coverage_rate",
            "taxonomy_coverage_rate",
            "boundary_value_coverage_rate",
            "data_feature_coverage_rate"
          ],
          "properties": {
            "scenario_coverage_rate": {
              "$ref": "#/definitions/rated_metric",
              "description": "Fraction of user scenarios covered by at least one test."
            },
            "taxonomy_coverage_rate": {
              "$ref": "#/definitions/rated_metric",
              "description": "Coverage across the MFT/INV/DIR test taxonomy categories (minimum functionality, invariance, directional expectation)."
            },
            "boundary_value_coverage_rate": {
              "$ref": "#/definitions/rated_metric",
              "description": "Coverage of boundary and edge-case values (empty, null, max, min, overflow)."
            },
            "data_feature_coverage_rate": {
              "$ref": "#/definitions/rated_metric",
              "description": "Coverage of data-specific features (pagination, filtering, sorting, relationships)."
            }
          }
        },
        "execution_quality": {
          "type": "object",
          "description": "Metrics measuring how well the test suite executes against the implementation.",
          "required": [
            "pass_rate",
            "code_coverage",
            "assertion_density",
            "weak_assertion_ratio",
            "test_realism_ratio"
          ],
          "properties": {
            "pass_rate": {
              "$ref": "#/definitions/rated_metric",
              "description": "Fraction of tests that pass."
            },
            "code_coverage": {
              "$ref": "#/definitions/rated_metric",
              "description": "Line or branch coverage reported by the test runner."
            },
            "assertion_density": {
              "$ref": "#/definitions/rated_metric",
              "description": "Average number of assertions per test. Higher is better."
            },
            "weak_assertion_ratio": {
              "$ref": "#/definitions/rated_metric",
              "description": "Fraction of tests using only trivial assertions (e.g., expect(true).toBe(true)). Lower is better."
            },
            "test_realism_ratio": {
              "$ref": "#/definitions/rated_metric",
              "description": "Fraction of tests at realism level L2 or above."
            }
          }
        },
        "delivery_quality": {
          "type": "object",
          "description": "Metrics measuring whether the tests validate the right behavior.",
          "required": [
            "expectation_match_rate",
            "boundary_handling_rate",
            "regression_safety_score",
            "business_flow_coverage"
          ],
          "properties": {
            "expectation_match_rate": {
              "$ref": "#/definitions/rated_metric",
              "description": "Fraction of core requirement expectations correctly asserted. Must be 1.0 to pass."
            },
            "boundary_handling_rate": {
              "$ref": "#/definitions/rated_metric",
              "description": "Fraction of boundary conditions handled correctly by the implementation."
            },
            "regression_safety_score": {
              "$ref": "#/definitions/rated_metric",
              "description": "Confidence score that the test suite would catch regressions."
            },
            "business_flow_coverage": {
              "$ref": "#/definitions/rated_metric",
              "description": "Fraction of identified end-to-end business flows verified through external calls (HTTP/CLI/Browser). Must be 1.0 to pass."
            }
          }
        },
        "iteration_efficiency": {
          "type": "object",
          "description": "Metrics tracking the efficiency of the fix loop across rounds.",
          "required": ["fix_convergence_rate", "fix_introduction_rate"],
          "properties": {
            "fix_convergence_rate": {
              "$ref": "#/definitions/efficiency_metric",
              "description": "Rate at which fixes resolve failures. Triggers stop if below 0.2 for 2 consecutive rounds."
            },
            "fix_introduction_rate": {
              "$ref": "#/definitions/efficiency_metric",
              "description": "Rate at which fixes introduce new failures. Triggers stop if above 0.3."
            }
          }
        }
      }
    },
    "gate_result": {
      "type": "string",
      "enum": ["pass", "fix_and_retry", "stop_and_report"],
      "description": "Decision gate result. 'pass' means all quality gates cleared. 'fix_and_retry' means the Agent should attempt fixes and re-run. 'stop_and_report' means the fix loop should halt (convergence failure or anti-pattern)."
    },
    "failures_grouped": {
      "type": "array",
      "description": "Test failures grouped by root cause, ordered by cluster size (largest first). The Agent uses this to prioritize fix targets.",
      "items": {
        "type": "object",
        "required": ["cluster_name", "affected_tests", "count", "suggested_fix", "evidence"],
        "properties": {
          "cluster_name": {
            "type": "string",
            "description": "Short description of the shared root cause (e.g., 'missing input validation', 'incorrect error status codes')."
          },
          "affected_tests": {
            "type": "array",
            "items": { "type": "string" },
            "description": "List of fully qualified test names affected by this root cause."
          },
          "count": {
            "type": "integer",
            "minimum": 1,
            "description": "Number of tests in this cluster."
          },
          "suggested_fix": {
            "type": "string",
            "description": "Specific, actionable fix direction for the Agent (e.g., 'Add Zod validation middleware to POST /users endpoint')."
          },
          "evidence": {
            "type": "string",
            "description": "Error messages, stack traces, or behavioral patterns that led to this root cause diagnosis."
          }
        }
      }
    },
    "fix_history": {
      "type": "array",
      "description": "Accumulated history of all fix rounds. Grows with each iteration. Used in the final quality report to show improvement trajectory.",
      "items": {
        "type": "object",
        "required": ["round", "metrics_before", "fix_description", "metrics_after"],
        "properties": {
          "round": {
            "type": "integer",
            "minimum": 1,
            "description": "The fix loop round number this entry corresponds to."
          },
          "metrics_before": {
            "type": "object",
            "required": ["pass_rate", "fail_count"],
            "properties": {
              "pass_rate": { "type": "number", "minimum": 0, "maximum": 1 },
              "fail_count": { "type": "integer", "minimum": 0 }
            }
          },
          "fix_description": {
            "type": "string",
            "description": "Human-readable summary of what was changed in this round."
          },
          "metrics_after": {
            "type": "object",
            "required": ["pass_rate", "newly_passing", "newly_failing"],
            "properties": {
              "pass_rate": { "type": "number", "minimum": 0, "maximum": 1 },
              "newly_passing": { "type": "integer", "minimum": 0 },
              "newly_failing": { "type": "integer", "minimum": 0 }
            }
          }
        }
      }
    },
    "hidden_tests": {
      "type": "object",
      "required": ["total", "run", "results"],
      "description": "Hidden test suite metadata. Hidden tests are not executed during the fix loop to prevent overfitting. They are only run in Phase 4 (final validation).",
      "properties": {
        "total": {
          "type": "integer",
          "minimum": 0,
          "description": "Total number of hidden tests available."
        },
        "run": {
          "type": "boolean",
          "description": "Whether hidden tests were executed. false during Phase 3 fix loop; true in Phase 4 final validation."
        },
        "results": {
          "description": "Hidden test execution results. null during fix loop; populated object in Phase 4.",
          "oneOf": [
            { "type": "null" },
            {
              "type": "object",
              "required": ["pass_count", "fail_count"],
              "properties": {
                "pass_count": { "type": "integer", "minimum": 0 },
                "fail_count": { "type": "integer", "minimum": 0 },
                "failure_details": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "test_name": { "type": "string" },
                      "error": { "type": "string" }
                    }
                  }
                }
              }
            }
          ]
        }
      }
    },
    "next_action": {
      "type": "string",
      "description": "Human-readable description of what the Agent should do next (e.g., 'Fix the 3 tests in the missing input validation cluster by adding request body validation middleware')."
    },
    "anti_patterns_detected": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Names of anti-patterns detected in the current test suite (e.g., 'overfitting', 'test tunnel vision', 'brittle assertions', 'implementation coupling')."
    }
  },
  "definitions": {
    "rated_metric": {
      "type": "object",
      "required": ["value", "threshold", "status"],
      "description": "A metric with a value, pass/fail threshold, and computed status.",
      "properties": {
        "value": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Current metric value."
        },
        "threshold": {
          "type": "number",
          "description": "Minimum value required to pass."
        },
        "status": {
          "type": "string",
          "enum": ["pass", "fail"],
          "description": "Whether this metric meets its threshold."
        },
        "note": {
          "type": "string",
          "description": "Optional note about this metric (e.g., 'core_must_be_100')."
        }
      }
    },
    "efficiency_metric": {
      "type": "object",
      "required": ["value"],
      "description": "An iteration efficiency metric without a simple pass/fail threshold.",
      "properties": {
        "value": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Current metric value."
        },
        "note": {
          "type": "string",
          "description": "Behavioral note (e.g., 'triggers_stop_if_below_0.2_for_2_rounds')."
        }
      }
    }
  }
}
```

---

## 3. Populated Example

Below is a realistic feedback report from **Round 2** of the fix loop for a TypeScript/Express REST API project.

```json
{
  "round": 2,
  "project_context": {
    "language": "typescript",
    "framework": "express",
    "test_runner": "vitest",
    "realism_level": "L2"
  },
  "metrics": {
    "design_quality": {
      "scenario_coverage_rate": { "value": 1.0, "threshold": 1.0, "status": "pass" },
      "taxonomy_coverage_rate": { "value": 1.0, "threshold": 1.0, "status": "pass" },
      "boundary_value_coverage_rate": { "value": 0.70, "threshold": 0.90, "status": "fail" },
      "data_feature_coverage_rate": { "value": 0.83, "threshold": 0.85, "status": "pass" }
    },
    "execution_quality": {
      "pass_rate": { "value": 0.80, "threshold": 0.95, "status": "fail" },
      "code_coverage": { "value": 0.78, "threshold": 0.80, "status": "fail" },
      "assertion_density": { "value": 3.2, "threshold": 2.0, "status": "pass" },
      "weak_assertion_ratio": { "value": 0.05, "threshold": 0.10, "status": "pass" },
      "test_realism_ratio": { "value": 0.85, "threshold": 0.70, "status": "pass" }
    },
    "delivery_quality": {
      "expectation_match_rate": { "value": 0.91, "threshold": 1.0, "status": "fail", "note": "core_must_be_100" },
      "boundary_handling_rate": { "value": 0.60, "threshold": 0.90, "status": "fail" },
      "regression_safety_score": { "value": 1.0, "threshold": 1.0, "status": "pass" },
      "business_flow_coverage": { "value": 0.50, "threshold": 1.0, "status": "fail", "note": "core_must_be_100" }
    },
    "iteration_efficiency": {
      "fix_convergence_rate": { "value": 0.45, "note": "triggers_stop_if_below_0.2_for_2_rounds" },
      "fix_introduction_rate": { "value": 0.12, "note": "triggers_stop_if_above_0.3" }
    }
  },
  "gate_result": "fix_and_retry",
  "failures_grouped": [
    {
      "cluster_name": "missing input validation on POST /users and PUT /users/:id",
      "affected_tests": [
        "POST /users rejects empty request body with 400",
        "POST /users rejects invalid email format with 400",
        "PUT /users/:id rejects negative age with 400"
      ],
      "count": 3,
      "suggested_fix": "Add Zod validation schema for user creation and update payloads. Apply as Express middleware before route handlers. Validate email format, require non-empty name, enforce age >= 0 and <= 150.",
      "evidence": "All 3 tests expect HTTP 400 responses but receive HTTP 201 (POST) or HTTP 200 (PUT). The route handlers accept any input without validation. Error messages: 'Expected status 400, received 201', 'Expected status 400, received 201', 'Expected status 400, received 200'."
    },
    {
      "cluster_name": "incorrect error status codes for resource not found",
      "affected_tests": [
        "GET /users/:id returns 404 for non-existent user",
        "DELETE /users/:id returns 404 for non-existent user"
      ],
      "count": 2,
      "suggested_fix": "In GET and DELETE handlers for /users/:id, query the database before processing. If no user is found, return res.status(404).json({ error: 'User not found' }) instead of continuing with null/undefined user data.",
      "evidence": "Both tests expect HTTP 404 but receive HTTP 500. The handlers attempt to operate on undefined user objects causing uncaught errors. Stack traces show TypeError: Cannot read properties of undefined (reading 'id') at UserController.getUser and TypeError: Cannot read properties of undefined at UserController.deleteUser."
    }
  ],
  "fix_history": [
    {
      "round": 1,
      "metrics_before": { "pass_rate": 0.58, "fail_count": 21 },
      "fix_description": "Fixed authentication middleware import path, added missing Jest/Vitest globals configuration, corrected test fixture data to match actual database schema, and replaced hardcoded timeouts with proper async/await patterns.",
      "metrics_after": { "pass_rate": 0.68, "newly_passing": 8, "newly_failing": 2 }
    },
    {
      "round": 2,
      "metrics_before": { "pass_rate": 0.68, "fail_count": 13 },
      "fix_description": "Fixed repository layer to use correct Prisma model names, added proper error handling in service layer for database connection failures, and corrected test assertions to match actual API response format.",
      "metrics_after": { "pass_rate": 0.80, "newly_passing": 9, "newly_failing": 1 }
    }
  ],
  "hidden_tests": {
    "total": 12,
    "run": false,
    "results": null
  },
  "next_action": "Prioritize the 'missing input validation' cluster (3 tests). Add a Zod validation schema for user creation/update payloads and wire it as Express middleware. Then address the 'incorrect error status codes' cluster (2 tests) by adding existence checks before route handler logic. Both clusters relate to defensive programming gaps.",
  "anti_patterns_detected": [
    "happy_path_obsession",
    "weak_assertions"
  ]
}
```

---

## 4. Usage Notes

### Generation

This report is generated by the AI Agent **after each test execution round**. The Agent collects test output, code coverage data, and design analysis results, then structures them according to this schema. The report is stored alongside the project artifacts and passed back to the Agent's decision loop.

### How the Agent Parses the Report

| Field | How the Agent Uses It |
|---|---|
| `failures_grouped` | Parses clusters in order (largest first). Each cluster's `suggested_fix` becomes a fix task. `evidence` helps the Agent understand *why* the failure occurred. |
| `gate_result` | Directly controls the loop: `"pass"` exits to Phase 4, `"fix_and_retry"` triggers another fix round, `"stop_and_report"` halts and produces a quality report. |
| `metrics` | The Agent checks `status` fields to understand which quality dimensions still need work. `design_quality` failures may require adding new tests; `execution_quality` failures require fixing existing tests or implementation. |
| `iteration_efficiency` | The Agent monitors convergence. If `fix_convergence_rate` drops below 0.2 for 2 rounds, or `fix_introduction_rate` exceeds 0.3, the Agent sets `gate_result` to `"stop_and_report"` regardless of other metrics. |
| `fix_history` | Accumulates across rounds. The Agent uses it to avoid repeating failed fix strategies and to measure improvement trajectory. It is included in the final quality report for human review. |
| `anti_patterns_detected` | If anti-patterns are present, the Agent adjusts its fix strategy. For example, `"overfitting"` causes the Agent to generalize assertions; `"implementation coupling"` causes it to test behavior rather than internals. |
| `next_action` | Serves as a natural language summary of the Agent's fix plan. Useful for logging and human review, but the Agent primarily relies on `failures_grouped` for concrete fix targets. |

### Hidden Tests Lifecycle

The `hidden_tests` section has a two-phase lifecycle:

1. **Phase 3 (Fix Loop):** `run` is `false`, `results` is `null`. Hidden tests are **never executed** during the fix loop to prevent the Agent from overfitting to specific test cases.
2. **Phase 4 (Final Validation):** `run` is `true`, `results` contains the pass/fail breakdown. If any hidden tests fail, the final report flags this as a critical finding.

### Machine-Parseability

The schema uses simple, flat JSON structures--no nested polymorphism or conditional logic beyond `hidden_tests.results`. This ensures the Agent can parse the report with straightforward property access without complex deserialization logic.

### Human-Readability

The `next_action` field, `cluster_name` fields, and `fix_description` entries in `fix_history` are written in natural language. When the final quality report is presented to a developer, these fields provide context without requiring them to read raw test output.
