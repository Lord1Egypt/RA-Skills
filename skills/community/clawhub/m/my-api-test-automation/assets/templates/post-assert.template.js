// Starter post-response assertion script

pm.test("HTTP status is successful", function () {
  pm.expect(pm.response.code).to.be.oneOf([200, 201, 202, 204]);
});

pm.test("Response time is under budget", function () {
  pm.expect(pm.response.responseTime).to.be.below(3000);
});

const json = pm.response.json();
pm.test("Business result code is success when present", function () {
  if (Object.prototype.hasOwnProperty.call(json, "code")) {
    pm.expect(json.code).to.be.oneOf([0, "0", "SUCCESS", 200]);
  }
});
