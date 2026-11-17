export default {
inject:['service', 'tags', 'ibf'],
data() {return {
    //报表数据:pid,name,workload,salary,subsidy,expense,resource,
    //receivable,income,iIncome,payable,pay,iPay
    list:[], 
    search:'',
    segs:this.tags.report.segs,
    ctrl:{cur:1, max:0}
}},
created(){
    this.ctrl.cur=this.ibf.getRt("cur",1);
    this.query(this.ctrl.cur);
},
methods:{
query(pg) {
    this.ibf.setRt("cur",pg);
    this.search='';
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var url = "/project/reports?offset="+offset+"&num="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK || resp.data.total==0) {
            this.list=[];
            this.ctrl.max=0;
            this.ctrl.cur=1;
            return;
        }
        this.list=resp.data.list.map(l=>{
            l.workload=(l.workload/1440).toFixed(2);
            return l;
        })
        this.ctrl.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
doSearch() {
    if(this.search=='') {
        this.query(this.ctrl.cur);
        return;
    }
    var url="/project/searchIds?s="+this.search+"&limit="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.list=[];
            this.ctrl.max=0;
            this.ctrl.cur=1;
            return;
        }
        var pids=resp.data.docs.filter(id => {
            return id>0;
        });
        var repUrl="/project/reports?pids="+pids.join(',')+"&num="+this.service.N_PAGE;
        request({method:"GET",url:repUrl}, this.service.name).then(resp1 => {
            if(resp1.code != RetCode.OK) {
                this.list=[];
                this.ctrl.max=0;
                this.ctrl.cur=1;
                return;
            }
            this.list=resp1.data.list.map(l=>{
                l.workload=(l.workload/1440).toFixed(2);
                return l;
            })
            this.ctrl.max=1;
            this.ctrl.cur=1;
        })
    })
},
detail(id) {
    this.service.goto("/project?id="+id)
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.report.title}}</q-toolbar-title>
   </q-toolbar>
  </q-header>
  <q-footer class="bg-white q-pa-sm">
    <q-input outlined v-model="search" :label="tags.search" dense @keyup.enter="doSearch">
     <template v-slot:append>
      <q-icon v-if="search!==''" name="close" @click="query(1)" class="cursor-pointer"></q-icon>
      <q-icon name="search" @click="doSearch"></q-icon>
     </template>
    </q-input>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-sm flex flex-center" v-show="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-markup-table flat>
 <thead><tr>
  <th>{{tags.report.prjName}}</th>
  <th>{{tags.report.in}}</th>
  <th>{{tags.report.out}}</th>
  <th>{{tags.report.salary}}</th>
  <th>{{segs.workload}}</th>
 </tr></thead>
 <tbody>
  <tr v-for="l in list" @click="detail(l.pid)" style="cursor:hand;">
  <td>{{l.name}}</td>
  <td>
   {{segs.income}}:{{l.income}}<br>
   {{segs.iIncome}}:{{l.iIncome}}<br>
   {{segs.receivable}}:{{l.receivable}}
  </td>
  <td>
   {{segs.pay}}:{{l.pay}}<br>
   {{segs.iPay}}:{{l.iPay}}<br>
   {{segs.payable}}:{{l.payable}}<br>
   {{segs.resource}}:{{l.resource}}
  </td>
  <td>
   {{segs.salary}}:{{l.salary}}<br>
   {{segs.subsidy}}:{{l.subsidy}}<br>
   {{segs.expense}}:{{l.expense}}
  </td>
  <td>{{l.workload}}</td>
  </tr>
 </tbody>
</q-markup-table>
  </q-page>
 </q-page-container>
</q-layout>
`
}