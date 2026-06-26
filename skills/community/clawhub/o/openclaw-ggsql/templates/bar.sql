-- Bar Chart Template
-- Required: x (categorical), y (numeric)
-- Optional: fill

SELECT {x_column}, {y_column}
{#if fill_column}  , {fill_column}{/if}
FROM '{data_source}'
{#if group_by}GROUP BY {group_by}{/if}
VISUALISE {x_column} AS x, {y_column} AS y
{#if fill_column}  , {fill_column} AS fill{/if}
DRAW bar
{#if scale_fill}SCALE {scale_fill} fill{/if}
LABEL
  title => '{title}',
  x => '{x_label}',
  y => '{y_label}'