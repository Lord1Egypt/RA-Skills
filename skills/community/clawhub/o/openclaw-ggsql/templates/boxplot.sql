-- Boxplot Template
-- Required: x (categorical), y (numeric)
-- Optional: fill

SELECT * FROM '{data_source}'
VISUALISE {x_column} AS x, {y_column} AS y
{#if fill_column}  , {fill_column} AS fill{/if}
DRAW boxplot
{#if scale_fill}SCALE {scale_fill} fill{/if}
LABEL
  title => '{title}',
  x => '{x_label}',
  y => '{y_label}'