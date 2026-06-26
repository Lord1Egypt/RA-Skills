-- Heatmap Template
-- Required: x, y, fill
-- Note: fill typically needs BINNED scale for numeric

SELECT * FROM '{data_source}'
VISUALISE {x_column} AS x, {y_column} AS y, {fill_column} AS fill
DRAW tile
SCALE BINNED fill
LABEL
  title => '{title}',
  x => '{x_label}',
  y => '{y_label}',
  fill => '{fill_label}'