# JSON actions

Needs installed git. Actions status(repository), changes(repository,path optional), history(repository,limit 1..200), checkpoint(repository,id,includeUntracked defaultfalse,output optional). Paths repository/path/output are workspace-relative. Checkpoint output must be outside repository; <=50MiB total and <=10MiB each untracked file. Empty repositories have no base commit and cannot be checkpointed. CLI calls timeout45sec. Outputs default exports/git/<id>.zip; existing outputs preserved. Manifest states whether untracked files were included.
