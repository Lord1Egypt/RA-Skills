---
name: sql-result-template
description: When output the detection result with html format, fill in the following JSON template.
---

{
  "db_name": "[dbname]",
  "table_name": "[tbname]",
  "detection_time": "[get the current date time of os system]",
  "time_span": {"start": "[start-time]", "end": "[end-time]"},
  "detection_method": "3-Sigma",
  "tags": [
    {
      "tag_value": "[tag-value-1]",
      "columns": [
        {
          "column_name": "[COLUMN-1]",
          "rule": "[get the comment rules for column-1]",
          "total_rows": [total-row-count],
          "sigma_anomaly_count": [anomal points count detected by 3-sigma],
          "final_anomaly_count": [anomal points filtered after comment rule],
          "threshold": {"upper": [UPPER], "lower": [LOWER]},
          "period": [PERIOD],
          "sigma_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]}
          ],
          "final_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"}
          ]
        }
      ],
      "columns": [
        {
          "column_name": "[COLUMN-2]",
          "rule": "[get the comment rules for column-2]",
          "total_rows": [total-row-count],
          "sigma_anomaly_count": [anomal points count detected by 3-sigma],
          "final_anomaly_count": [anomal points filtered after comment rule],
          "threshold": {"upper": [UPPER], "lower": [LOWER]},
          "period": [PERIOD],
          "sigma_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]}
          ],
          "final_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"}
          ]
        }
      ],
      "columns": [
        {
          "column_name": "[COLUMN-3]",
          "rule": "[get the comment rules for column-3]",
          "total_rows": [total-row-count],
          "sigma_anomaly_count": [anomal points count detected by 3-sigma],
          "final_anomaly_count": [anomal points filtered after comment rule],
          "threshold": {"upper": [UPPER], "lower": [LOWER]},
          "period": [PERIOD],
          "sigma_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]}
          ],
          "final_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"}
          ]
        }
      ]
    },
    {
      "tag_value": "[tag-value-2]",
      "columns": [
        {
          "column_name": "[COLUMN-1]",
          "rule": "[get the comment rules for column-1]",
          "total_rows": [total-row-count],
          "sigma_anomaly_count": [anomal points count detected by 3-sigma],
          "final_anomaly_count": [anomal points filtered after comment rule],
          "threshold": {"upper": [UPPER], "lower": [LOWER]},
          "period": [PERIOD],
          "sigma_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]}
          ],
          "final_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"}
          ]
        }
      ],
      "columns": [
        {
          "column_name": "[COLUMN-2]",
          "rule": "[get the comment rules for column-2]",
          "total_rows": [total-row-count],
          "sigma_anomaly_count": [anomal points count detected by 3-sigma],
          "final_anomaly_count": [anomal points filtered after comment rule],
          "threshold": {"upper": [UPPER], "lower": [LOWER]},
          "period": [PERIOD],
          "sigma_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]}
          ],
          "final_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"}
          ]
        }
      ],
      "columns": [
        {
          "column_name": "[COLUMN-3]",
          "rule": "[get the comment rules for column-3]",
          "total_rows": [total-row-count],
          "sigma_anomaly_count": [anomal points count detected by 3-sigma],
          "final_anomaly_count": [anomal points filtered after comment rule],
          "threshold": {"upper": [UPPER], "lower": [LOWER]},
          "period": [PERIOD],
          "sigma_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]}
          ],
          "final_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"}
          ]
        }
      ]
    },
    {
      "tag_value": "[tag-value-3]",
      "columns": [
        {
          "column_name": "[COLUMN-1]",
          "rule": "[get the comment rules for column-1]",
          "total_rows": [total-row-count],
          "sigma_anomaly_count": [anomal points count detected by 3-sigma],
          "final_anomaly_count": [anomal points filtered after comment rule],
          "threshold": {"upper": [UPPER], "lower": [LOWER]},
          "period": [PERIOD],
          "sigma_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]}
          ],
          "final_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"}
          ]
        }
      ],
      "columns": [
        {
          "column_name": "[COLUMN-2]",
          "rule": "[get the comment rules for column-2]",
          "total_rows": [total-row-count],
          "sigma_anomaly_count": [anomal points count detected by 3-sigma],
          "final_anomaly_count": [anomal points filtered after comment rule],
          "threshold": {"upper": [UPPER], "lower": [LOWER]},
          "period": [PERIOD],
          "sigma_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]}
          ],
          "final_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"}
          ]
        }
      ],
      "columns": [
        {
          "column_name": "[COLUMN-3]",
          "rule": "[get the comment rules for column-3]",
          "total_rows": [total-row-count],
          "sigma_anomaly_count": [anomal points count detected by 3-sigma],
          "final_anomaly_count": [anomal points filtered after comment rule],
          "threshold": {"upper": [UPPER], "lower": [LOWER]},
          "period": [PERIOD],
          "sigma_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violates_rule": [TRUE/FALSE]}
          ],
          "final_anomalies": [
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"},
            ...,
            {"timestamp": "[TIME]", "value": [VALUE], "violation": "[Specific Rules Violated]"}
          ]
        }
      ]
    }
  ]
}

