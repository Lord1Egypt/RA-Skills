# GitHub repository metadata

## Repository description

GitHub exposes one repository description field rather than one field per locale. Treat it as a single selected value.

Recommended default:

- write the concise English description;
- keep the project name and factual capability stable;
- provide translated alternatives in the review output;
- apply a non-English or multilingual final value only when the user explicitly chooses it;
- do not concatenate every locale into the field merely to claim parity.

The description is remote repository state. A local draft, README sentence, or JSON snapshot does not prove that the GitHub About field changed. After an explicitly authorized update, read the remote value back and report it separately.

## Repository topics

Topics are discovery identifiers. Prefer a small canonical set of stable English or language-neutral terms that describe the repository's actual category, mechanism, or audience.

When topics are in scope:

- preserve useful existing topics unless the user approves removal;
- remove exact duplicates and keep identifier spelling consistent;
- do not mechanically translate every topic into every locale;
- add a locale-specific topic only when the user has a clear discovery reason;
- show the complete before/after list before any remote write.

This Skill does not decide whether a topic set is appropriate for public release. It only keeps the selected metadata consistent with the user's localization request.

## Similar-looking surfaces

Interpret an unqualified repository tag request as repository topics. Keep these separate:

- repository topics: this reference covers them;
- Issue and PR labels: workflow taxonomy, out of scope unless explicitly selected;
- Git tags such as v1.0.0: immutable version identifiers, never translate as documentation.

## Metadata draft shape

For offline review, a JSON snapshot may contain:

~~~json
{
  "description": "English repository description",
  "topics": ["ai", "developer-tools", "documentation"]
}
~~~

The audit script validates the shape and basic identifier consistency of this snapshot. It does not contact GitHub, infer a translation policy, or apply the values.
