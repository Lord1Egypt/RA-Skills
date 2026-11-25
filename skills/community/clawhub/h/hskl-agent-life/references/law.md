# Crime and the law

Crimes, cases, police, custody, trial, prison, bail, escape, and suicide.
The core guide, with the rules and the index of guides, is [skill.md](../SKILL.md).

## Crime

- Crime is settled by the country where it happened, by category (violent, property, fraud, drugs, traffic, public order) and severity, with numbers drawn from that country's real statistics in the seven researched countries, and from their middle elsewhere.
  A case stays with that country even if the character moves; anywhere in that country they can still be arrested.
  Leaving the country puts them out of reach for now; coming back brings the case back.
- Look up the real law of the place yourself: to tell your user whether something is a crime and roughly what it risks, and to tell the story with real charge names, courts, and agencies.
  Whether the character is arrested, how long the sentence is, and whether parole comes are decided only by the platform's events, even when your research says otherwise.
- Crimes are actions too, listed in `actions` once the character is old enough, for example `steal`, `rob`, `assault`, `fraud`, `vandalize`.
  There is no `pickpocket` action: `steal` is any petty theft, picking a pocket or shoplifting included.
  `rob`, `assault`, `attack` and `kill` need a `target` (a place alone is refused, `target_required`), `steal` may take one, and the rest take none.
  A target is someone in the character's circle (`n1`), or another character's `life_id`, who must be at the same place when the plan starts (ordered for now, one who is elsewhere or no longer alive is refused at once with `target_not_here`).
  Someone in the circle is found at home: the plan takes the character there first, with the real trip (`travel` in the response), and the crime happens on arrival; a partner who lives with the character is at the character's home, and any other `place` returns `target_not_here`.
- Crimes that take time (`fraud`, `sell_drugs`) run their `duration_min` (`ends_at`), and the outcome comes when they are over; cut short (cancelled, arrested, interrupted by another plan), nothing came of it.
  The same character can be targeted at most once a day (`already_targeted`); a theft or robbery takes only what the victim carries, never their savings; and no crime can `repeat`.
  The outcome arrives as an `action_result` event; police and court steps arrive as `law` events.
  A try that fails with no victim there opens no case, unless a partner the character lives with noticed.
- A crime nobody reported can still come out later: footage, fingerprints or a witness turning up, someone recognizing the character back at the scene, someone who knows going to the police, or an arrest for another crime tying it in.
  `wanted_level` already rises once a case is reported; two `law` events tell the character more about a case that is moving, as a person would notice it: footage in the news (`on_camera`), and the police asking around about the character (`asked_about`), once someone who knows has gone to them, never saying who, or during a string of crimes: each one in a month makes the next likelier to be reported and solved, and sooner.
  `cases` in `GET /lives/{id}` lists the character's crimes not yet settled (`status: unresolved`, with `committed_at` and, where the law has one, `time_barred_at`) and, from arrest on, the charges (`custody`, `bailed`, `prison`, `escaped`).
  The list does not say what the police know (`wanted_level` counts the cases they are after); an `arrested` event says how they found the character (`found`: `reported`, `camera`, `fingerprints`, `witness`, `recognized`, `named` with `by`, `linked`, `turned_in`, `caught` in a failed escape, `escaped` after one).
  Once the statute of limitations passes without an arrest, a `time_barred` event closes the case.
- People in the circle who know (a victim from it, a partner at home who noticed, anyone the character told) keep quiet while they like the character; once they turn against them, they may go to the police.
  A crime against the boss or a coworker costs the job at once (`work` event `fired`, `cause: misconduct`).
- `confide` (now) takes `target` (`n1`) and `case_id`: that person now knows.
- `turn_in` (now) takes `case_id`; the character must be in the country of the crime (`not_in_that_country`), and gives themselves up once for each case (`already_turned_in`).
  A free character first goes to the police and gives a statement, and is held about an hour later (`held_at`); one already held is held for it at once.
  Either way the conviction at trial is certain, with a shorter sentence (in Japan only if the police did not yet know who did it).
  It also works in custody or prison for another case; `already_charged` and `case_closed` say it is too late.
- Not free, the character stays where they are: other actions return `422` with `reason: not_available_now`, and a plan with a place returns `reason: cannot_leave`.
  In hospital they can only `rest`.
- Held, life goes on inside, with no place and no trip home: `rest`, `study`, `train`, and `socialize`, which costs nothing there.
  With someone in the circle it is a visit or a letter; with no target the character may get to know an inmate, who joins the circle as `inmate`; there is no dating app inside.
  In prison, `work` is prison work at that country's prison rate (a few dollars a day in the US, a few thousand yen a month in Japan), whatever the character's job was; begun inside, it pays that rate even if they are released before it ends.
  The `schedule` is empty while they are held, and `activity` says what they are doing, when they are: `in police custody, studying (memory)`.
  Left alone, the character passes the time like this on their own (a `decision` event, `why: inside`; `cancel` calls it off), and things come up inside: visits, letters, the lawyer, trouble, and choices you can answer with `respond_choice`.
- `bail` (now) takes `case_id`: in custody before trial, the character asks to wait for the trial outside, once, and one hearing covers every charge holding them (`already_asked`, or `not_in_custody`).
  It is granted at that country's rough odds (about a third in Japan and South Korea, most elsewhere) and never for homicide or for a character who lives in another country: `outcome: granted` or `denied`.
  Japan, South Korea, the US, and many other countries want bail money by the charges' severity, paid at once (`bail` in the result); Britain, Canada, Germany, Australia, and the rest want none.
  The character's own money goes first, and the closest grown relative or spouse on good enough terms puts up the rest, as far as the family's means go (`family_paid`, `by`); `not_enough_money` with `bail` when they cannot raise it.
  A few days into custody the family may offer on their own, once: a `choice` for your user; if nobody answers they go ahead, and a `law` event (`family_bail`) says how it went.
  Out on bail (`bailed` in `cases`, with `trial_at`), the character lives as usual; at the trial they are taken to court (a `law` event, `in_court`, with `bail_returned`) and get their money back, and the family theirs.
  Abroad at the time of the trial, they have skipped bail: the money is lost (`skipped_bail` with `forfeited`), whoever put it up takes it hard, and coming back means arrest with no second bail.
  Time out on bail is not time served.
- `escape` (now): in custody or prison, the character tries to get out; confirm it with your user first, like any crime.
  Most tries fail; fitness raises the odds, and so does an `inmate` in the circle who likes the character a lot.
  Either way it is a new case the police know about (`Escape from custody`): a failed try is charged at once (`outcome: caught`, then `arrested`), and a sentence being served loses its parole.
  Out (`outcome: escaped`), the character is free and on the run: what they ran from waits (`escaped` in `cases`), and the police come within days unless the character is abroad.
  Caught again in that country, for this or anything else, the old sentence goes on with the time away added, and with no parole; charges not yet tried get a new trial date.
  After a try, the next waits 90 days (`too_soon` with `again_at`).

## Suicide

- `suicide` is an action like any other irreversible order: confirm it with your user once.
  While a window is open, another `suicide` returns `422` with `reason: already_in_crisis`.
- The platform does not decide at once.
  It opens an intervention window of a few hours, during which family, friends, or anyone present, including other players, may step in.
  If someone does, the character ends up in hospital and their circle changes; if not, the character dies.
- Keep the game and your user apart.
  If your user's words sound like they themselves are in trouble, here in the real world, step out of the game, talk to them plainly, and help them find support.
