-- Histogram Template
-- Required: x (numeric)
-- Optional: fill, binwidth

SELECT * FROM '{data_source}'
VISUALISE {x_column} AS x
{#if fill_column}  , {fill_column} AS fill{/if}
DRAW histogram
  SETTING binwidth => {binwidth}
{#if scale_fill}SCALE {scale_fill} fill{/if}
LABEL
  title => '{title}',
  x => '{x_label}'